from typing import Any

from typing_extensions import TypedDict


class HTTPRequestData(TypedDict, total=False):
    method: str
    url: str
    headers: dict[str, str]
    params: dict[str, Any]
    json_body: Any
    body: str
    timeout_seconds: float
    follow_redirects: bool
    max_response_chars: int


class HTTPResponseData(TypedDict, total=False):
    request: HTTPRequestData
    response: dict[str, Any]
