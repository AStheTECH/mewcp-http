import base64
from typing import Any

import httpx

from .config import (
    ALLOWED_HTTP_METHODS,
    DEFAULT_TIMEOUT_SECONDS,
    MAX_RESPONSE_BODY_CHARS,
)
from .schemas import HTTPResponseData


def _serialize_headers(headers: dict[str, Any] | None) -> dict[str, str]:
    if not headers:
        return {}
    return {str(key): str(value) for key, value in headers.items()}


def _serialize_text_body(content: str, max_response_chars: int) -> dict[str, Any]:
    is_truncated = len(content) > max_response_chars
    body = content[:max_response_chars] if is_truncated else content
    return {
        "kind": "text",
        "content": body,
        "truncated": is_truncated,
        "original_length": len(content),
    }


def _serialize_binary_body(content: bytes, max_response_chars: int) -> dict[str, Any]:
    is_truncated = len(content) > max_response_chars
    body = content[:max_response_chars] if is_truncated else content
    return {
        "kind": "base64",
        "content": base64.b64encode(body).decode("ascii"),
        "truncated": is_truncated,
        "original_length": len(content),
    }


def _serialize_response_body(
    response: httpx.Response,
    max_response_chars: int,
) -> dict[str, Any]:
    content_type = response.headers.get("content-type", "").lower()

    if "application/json" in content_type:
        try:
            parsed_json = response.json()
        except ValueError:
            parsed_json = None
        text_payload = _serialize_text_body(response.text, max_response_chars)
        if parsed_json is not None:
            text_payload["json"] = parsed_json
        return text_payload

    if content_type.startswith("text/") or "xml" in content_type or "html" in content_type:
        return _serialize_text_body(response.text, max_response_chars)

    return _serialize_binary_body(response.content, max_response_chars)


def execute_http_request(
    method: str,
    url: str,
    headers: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    json_body: Any | None = None,
    body: str | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    follow_redirects: bool = True,
    max_response_chars: int = MAX_RESPONSE_BODY_CHARS,
) -> HTTPResponseData:
    normalized_method = method.upper().strip()

    if normalized_method not in ALLOWED_HTTP_METHODS:
        raise ValueError(
            "method must be one of: " + ", ".join(sorted(ALLOWED_HTTP_METHODS))
        )

    if not url.lower().startswith(("http://", "https://")):
        raise ValueError("url must start with 'http://' or 'https://'")

    if json_body is not None and body is not None:
        raise ValueError("Provide only one of 'json_body' or 'body'")

    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than 0")

    if max_response_chars <= 0:
        raise ValueError("max_response_chars must be greater than 0")

    request_headers = _serialize_headers(headers)

    try:
        with httpx.Client(
            follow_redirects=follow_redirects,
            timeout=timeout_seconds,
        ) as client:
            response = client.request(
                method=normalized_method,
                url=url,
                headers=request_headers,
                params=params,
                json=json_body,
                content=body,
            )
    except httpx.HTTPError as exc:
        raise RuntimeError(f"HTTP request failed: {exc}") from exc

    return {
        "request": {
            "method": normalized_method,
            "url": url,
            "headers": request_headers,
            "params": params or {},
            "timeout_seconds": timeout_seconds,
            "follow_redirects": follow_redirects,
            "max_response_chars": max_response_chars,
        },
        "response": {
            "url": str(response.url),
            "status_code": response.status_code,
            "reason_phrase": response.reason_phrase,
            "headers": dict(response.headers),
            "elapsed_ms": round(response.elapsed.total_seconds() * 1000, 2),
            "body": _serialize_response_body(response, max_response_chars),
        },
    }
