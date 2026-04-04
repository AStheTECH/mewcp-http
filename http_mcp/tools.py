import json
import logging
from typing import Any

from fastmcp import FastMCP
from pydantic import Field

from .config import DEFAULT_TIMEOUT_SECONDS, MAX_RESPONSE_BODY_CHARS
from .service import execute_http_request

logger = logging.getLogger("http-mcp-server")


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool(
        name="health_check",
        description="Check server readiness.",
    )
    def health_check() -> str:
        return json.dumps({"status": "ok", "server": "CL HTTP MCP Server"})

    @mcp.tool(
        name="http_request",
        description="Perform a generic HTTP/HTTPS request and return status, headers, and body.",
    )
    def http_request(
        method: str = Field(..., description="HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)"),
        url: str = Field(..., description="Target URL beginning with http:// or https://"),
        headers: dict[str, str] | None = Field(default=None, description="Optional HTTP headers"),
        params: dict[str, Any] | None = Field(default=None, description="Optional query parameters"),
        json_body: Any | None = Field(default=None, description="Optional JSON request body"),
        body: str | None = Field(default=None, description="Optional raw string request body"),
        timeout_seconds: float = Field(
            default=DEFAULT_TIMEOUT_SECONDS,
            description="HTTP timeout in seconds",
        ),
        follow_redirects: bool = Field(
            default=True,
            description="Whether to follow HTTP redirects",
        ),
        max_response_chars: int = Field(
            default=MAX_RESPONSE_BODY_CHARS,
            description="Maximum response characters/bytes to return in the body field",
        ),
    ) -> str:
        try:
            result = execute_http_request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json_body=json_body,
                body=body,
                timeout_seconds=timeout_seconds,
                follow_redirects=follow_redirects,
                max_response_chars=max_response_chars,
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed http_request for '{url}': {e}")
            return json.dumps({"error": str(e)})
