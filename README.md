**Send generic HTTP requests and get normalized API responses via MCP.**

A Model Context Protocol (MCP) server that exposes HTTP/HTTPS request execution for testing APIs, integrating web services, and fetching remote data in agent workflows.

---

## Overview

The CL HTTP MCP Server provides stateless, auth-agnostic HTTP access:

- Multi-method request execution (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
- Flexible request shaping with headers, query params, and JSON/raw bodies
- Structured response payloads with metadata, truncation handling, and JSON/body normalization

Perfect for:

- Calling external REST APIs from MCP-compatible clients
- Testing webhooks and endpoint integrations quickly
- Retrieving remote content in automations and multi-agent systems

---

## Tools

<details>
<summary><code>health_check</code> — Check server readiness</summary>

Returns a lightweight readiness payload so clients can verify the server is up.

**Inputs:**

- None

**Output:**

```json
{
  "status": "ok",
  "server": "CL HTTP MCP Server"
}
```

**Usage Example:**

```bash
POST /mcp/http/health_check

{}
```

</details>

---

<details>
<summary><code>http_request</code> — Execute an HTTP/HTTPS request</summary>

Performs an outbound HTTP call and returns normalized request/response details, including status, headers, elapsed time, and serialized body content.

**Inputs:**

- `method` (string, required) — HTTP method (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`)
- `url` (string, required) — Absolute target URL starting with `http://` or `https://`
- `headers` (object, optional) — Request headers as key/value pairs
- `params` (object, optional) — Query-string parameters as key/value pairs
- `json_body` (any, optional) — JSON payload body
- `body` (string, optional) — Raw string payload body (cannot be used with `json_body`)
- `timeout_seconds` (number, optional) — HTTP timeout in seconds (default: `30.0`)
- `follow_redirects` (boolean, optional) — Whether redirects are followed (default: `true`)
- `max_response_chars` (integer, optional) — Maximum body characters/bytes returned (default: `50000`)

**Output:**

```json
{
  "request": {
    "method": "GET",
    "url": "https://httpbin.org/get",
    "headers": {
      "accept": "application/json"
    },
    "params": {
      "source": "cl-mcp-http"
    },
    "timeout_seconds": 30.0,
    "follow_redirects": true,
    "max_response_chars": 50000
  },
  "response": {
    "url": "https://httpbin.org/get?source=cl-mcp-http",
    "status_code": 200,
    "reason_phrase": "OK",
    "headers": {
      "content-type": "application/json"
    },
    "elapsed_ms": 94.17,
    "body": {
      "kind": "text",
      "content": "{...}",
      "truncated": false,
      "original_length": 312,
      "json": {
        "args": {
          "source": "cl-mcp-http"
        }
      }
    }
  }
}
```

**Usage Example:**

```bash
POST /mcp/http/http_request

{
  "method": "GET",
  "url": "https://httpbin.org/get",
  "headers": {
    "accept": "application/json"
  },
  "params": {
    "source": "cl-mcp-http"
  }
}
```

</details>

---

<details>
<summary><strong>API Parameters Reference</strong></summary>

### Common Parameters

- `timeout_seconds` — Maximum time (in seconds) allowed for the HTTP request
- `follow_redirects` — Controls whether 3xx redirects are automatically followed
- `max_response_chars` — Limits response body size returned by the tool

### Resource Formats

**URL Input:**

```text
https://{host}/{path}?{query}
Example: https://api.example.com/v1/items?limit=10
```

**Response Body Object:**

```text
kind: text | base64
content: string
truncated: boolean
original_length: integer
json: object (only for parseable JSON responses)
```

</details>

---

<details>
<summary><strong>Troubleshooting</strong></summary>

### **Invalid URL Format**

- **Cause:** `url` does not start with `http://` or `https://`
- **Solution:**
  1. Provide a full absolute URL (including protocol)
  2. Verify no typos in host/path

### **Unsupported HTTP Method**

- **Cause:** `method` is outside allowed set
- **Solution:**
  1. Use one of: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`
  2. Ensure method is passed as a string

### **Conflicting Body Inputs**

- **Cause:** Both `json_body` and `body` are provided in the same request
- **Solution:**
  1. Use `json_body` for JSON payloads
  2. Use `body` for raw text payloads
  3. Send only one body field per call

### **Timeout or Upstream Network Errors**

- **Cause:** Slow endpoint, network issues, or unreachable host
- **Solution:**
  1. Increase `timeout_seconds` for long-running endpoints
  2. Confirm endpoint is publicly reachable
  3. Retry with reduced payload or simplified query parameters

### **Response Body Appears Truncated**

- **Cause:** Response size exceeded `max_response_chars`
- **Solution:**
  1. Increase `max_response_chars` if larger output is required
  2. Request smaller payloads with filters/pagination from the upstream API

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[HTTP Methods Reference (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)** — Official method behavior documentation
- **[HTTP Status Codes (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)** — Standard HTTP response status reference
- **[httpx Documentation](https://www.python-httpx.org/)** — Python HTTP client used by this server
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP framework and protocol usage

</details>

---

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
