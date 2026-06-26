"""Shared error helpers for all tool modules."""

import httpx
from ..logging_utils import ToolLogger
from ..schemas import ToolError


def _err(result_class, tlog, code, message, status, retriable=False, retry_after=None):
    tlog.failure(code, message)
    return result_class(
        success=False, statusCode=status, retriable=retriable,
        retry_after_seconds=retry_after,
        error=ToolError(code=code, message=message),
    )


def _handle_request_exc(result_class, tlog, exc):
    if isinstance(exc, httpx.ConnectTimeout):
        tlog.failure("UPSTREAM_ERROR", "Connection timeout")
        return result_class(success=False, statusCode=408, retriable=False,
            error=ToolError(code="UPSTREAM_ERROR", message="Connection timeout"))
    if isinstance(exc, httpx.ReadTimeout):
        tlog.failure("UPSTREAM_ERROR", "Read timeout")
        return result_class(success=False, statusCode=504, retriable=False,
            error=ToolError(code="UPSTREAM_ERROR", message="Read timeout"))
    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        tlog.failure("UPSTREAM_ERROR", f"HTTP {status}")
        return result_class(success=False, statusCode=503, retriable=True,
            error=ToolError(code="UPSTREAM_ERROR", message=str(exc)))
    if isinstance(exc, httpx.HTTPError):
        tlog.failure("UPSTREAM_ERROR", str(exc))
        return result_class(success=False, statusCode=503, retriable=True,
            error=ToolError(code="UPSTREAM_ERROR", message=str(exc)))
    if isinstance(exc, ValueError):
        tlog.failure("VALIDATION_ERROR", str(exc))
        return result_class(success=False, statusCode=400, retriable=False,
            error=ToolError(code="VALIDATION_ERROR", message=str(exc)))
    tlog.failure("SERVER_ERROR", str(exc))
    return result_class(success=False, statusCode=500, retriable=False,
        error=ToolError(code="SERVER_ERROR", message=str(exc)))
