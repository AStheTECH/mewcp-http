# CL HTTP MCP Server

A Model Context Protocol (MCP) utility server that performs generic HTTP/HTTPS requests and returns normalized response data.

## Authentication

This is a utility MCP. Authentication is not required by server tools.

The server is stateless and does not store per-user session or auth state in memory.

## Features

- `health_check`: Returns server readiness status.
- `http_request`: Executes an HTTP/HTTPS request with configurable method, headers, params, and body.

## Available Tools

### health_check

- Description: Check server readiness.
- Inputs: None.

### http_request

- Description: Perform a generic HTTP/HTTPS request and return status, headers, and body.
- Inputs:
  - `method` (required): HTTP method. Allowed values: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS.
  - `url` (required): Target URL beginning with `http://` or `https://`.
  - `headers` (optional): Key-value HTTP headers.
  - `params` (optional): Key-value query parameters.
  - `json_body` (optional): JSON request body.
  - `body` (optional): Raw string request body. Cannot be used with `json_body` in the same call.
  - `timeout_seconds` (optional): Request timeout in seconds. Default: 30.0.
  - `follow_redirects` (optional): Follow redirects. Default: true.
  - `max_response_chars` (optional): Maximum response characters/bytes returned in body content. Default: 50000.

Example body JSON for `http_request`:

```json
{
  "tool": "http_request",
  "arguments": {
    "method": "GET",
    "url": "https://httpbin.org/get",
    "headers": {
      "accept": "application/json"
    },
    "params": {
      "source": "cl-mcp-http"
    }
  }
}
```

## Setup

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
# stdio
python server.py

# sse
python server.py --transport sse --host 127.0.0.1 --port 8001

# streamable-http
python server.py --transport streamable-http --host 127.0.0.1 --port 8001
```

## Project Structure

```text
cl-mcp-http/
|-- server.py
|-- requirements.txt
|-- README.md
`-- http_mcp/
    |-- __init__.py
    |-- cli.py
    |-- config.py
    |-- tools.py
    |-- schemas.py
    `-- service.py
```
