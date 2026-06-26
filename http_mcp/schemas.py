"""Pydantic schemas for MewCP HTTP MCP Server."""

from typing import Any

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# Base classes — copy verbatim into every MewCP server
# ---------------------------------------------------------------------------

class ToolError(BaseModel):
    code: str
    message: str
    details: Any = None


class ToolResult(BaseModel):
    success: bool
    statusCode: int
    retriable: bool = False
    retry_after_seconds: int | None = None
    error: ToolError | None = None


# ---------------------------------------------------------------------------
# health_check tool
# ---------------------------------------------------------------------------

class HttpCheckData(BaseModel):
    model_config = ConfigDict(extra="allow")

    status: str
    server: str


class HttpCheckResult(ToolResult):
    data: HttpCheckData | None = None


# ---------------------------------------------------------------------------
# http_request tool
# ---------------------------------------------------------------------------

class HttpResponseBodyData(BaseModel):
    model_config = ConfigDict(extra="allow")

    kind: str
    content: str
    truncated: bool
    original_length: int
    json: Any = None


class HttpRequestEchoData(BaseModel):
    model_config = ConfigDict(extra="allow")

    method: str
    url: str
    headers: dict[str, str]
    params: dict[str, Any] = {}
    timeout_seconds: float
    follow_redirects: bool
    max_response_chars: int


class HttpResponseInnerData(BaseModel):
    model_config = ConfigDict(extra="allow")

    url: str
    status_code: int
    reason_phrase: str
    headers: dict[str, str]
    elapsed_ms: float
    body: HttpResponseBodyData


class HttpRequestResultData(BaseModel):
    model_config = ConfigDict(extra="allow")

    request: HttpRequestEchoData
    response: HttpResponseInnerData


class HttpRequestResult(ToolResult):
    data: HttpRequestResultData | None = None
