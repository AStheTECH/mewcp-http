"""MewCP HTTP tool registration."""

from fastmcp import FastMCP

from .http_tools import register_http_tools


def register_tools(mcp: FastMCP) -> None:
    register_http_tools(mcp)
