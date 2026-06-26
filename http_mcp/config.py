"""Configuration for MewCP HTTP MCP Server."""

import logging
import os

SERVER_VERSION = "v1.1.0"
BREAKING_CHANGES: list[dict] = []

# Per-request timeout supplied by caller; this is the fallback default
DEFAULT_TIMEOUT_SECONDS = 30.0
CONNECT_TIMEOUT = 5  # TCP connection — fixed, API-independent
MAX_RESPONSE_BODY_CHARS = 50000
ALLOWED_HTTP_METHODS = {
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "HEAD",
    "OPTIONS",
}


def configure_logging() -> None:
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    try:
        from pythonjsonlogger import jsonlogger

        handler = logging.StreamHandler()
        handler.setFormatter(
            jsonlogger.JsonFormatter(
                fmt="%(asctime)s %(name)s %(levelname)s %(message)s"
            )
        )
    except ImportError:
        handler = logging.StreamHandler()
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(log_level)
