**Send generic HTTP requests and get normalized API responses via MCP.**

A Model Context Protocol (MCP) server that exposes HTTP/HTTPS request execution for testing APIs, integrating web services, and fetching remote data in agent workflows.


## Overview

The MewCP HTTP MCP Server provides stateless, auth-agnostic HTTP access:

- Multi-method request execution (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
- Flexible request shaping with headers, query params, and JSON/raw bodies
- Structured response payloads with metadata, truncation handling, and JSON/body normalization

Perfect for:

- Calling external REST APIs from MCP-compatible clients
- Testing webhooks and endpoint integrations quickly
- Retrieving remote content in automations and multi-agent systems


## Auth

No credentials required. This server is auth-agnostic — pass any authentication material (API keys, bearer tokens, etc.) directly via the `headers` parameter on each request.


## Tools


<details>
<summary><code>http_request</code> — Perform a generic HTTP/HTTPS request and return status, headers, and body.</summary>

Perform a generic HTTP/HTTPS request and return status, headers, and body.

**Inputs:**
```
- `method` (string, required) — HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
- `url` (string, required) — Target URL beginning with http:// or https://
- `headers` (object, optional) — Optional HTTP headers as a dict of string key/value pairs. Omit to send no custom headers.
- `params` (object, optional) — Optional query parameters as a dict; appended to the URL as ?key=value pairs. Omit to send no query string.
- `json_body` (any, optional) — Optional JSON request body (any JSON-serializable value). Mutually exclusive with `body`. Omit for requests with no body.
- `body` (string, optional) — Optional raw string request body. Mutually exclusive with `json_body`. Omit for requests with no body.
- `timeout_seconds` (number, optional, default: 30.0) — Read timeout in seconds for the HTTP request. Defaults to 30.0s if omitted. Increase for slow endpoints.
- `follow_redirects` (boolean, optional, default: true) — Whether to follow HTTP 3xx redirects automatically. Defaults to true if omitted.
- `max_response_chars` (integer, optional, default: 50000) — Maximum response body characters or bytes to return. Defaults to 50000 if omitted. Increase to retrieve larger responses.
```

**Output `data` schema:**

```typescript
{
  request: {
    method: string;
    url: string;
    headers: { [key: string]: string };
    params: { [key: string]: any };
    timeout_seconds: number;
    follow_redirects: boolean;
    max_response_chars: number;
  };
  response: {
    url: string;
    status_code: number;
    reason_phrase: string;
    headers: { [key: string]: string };
    elapsed_ms: number;
    body: {
      kind: string;
      content: string;
      truncated: boolean;
      original_length: number;
      json: any | null;
    };
  };
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Response Envelope</strong></summary>

Every tool returns the same top-level envelope. Only `data` varies per tool.

```json
// Success
{
  "success": true,
  "statusCode": 200,
  "retriable": false,
  "retry_after_seconds": null,
  "error": null,
  "data": { ... }
}

// Error
{
  "success": false,
  "statusCode": 400,
  "retriable": false,
  "retry_after_seconds": null,
  "error": { "code": "VALIDATION_ERROR", "message": "{description}", "details": {} },
  "data": null
}
```

- `retriable` — `true` when it is safe to retry (rate limit, network error, 503). `false` for validation and auth errors.
- `retry_after_seconds` — seconds to wait before retrying; present only when `retriable` is `true` and the upstream specifies a delay.
- `error.code` — machine-readable string: `VALIDATION_ERROR`, `AUTH_ERROR`, `UPSTREAM_ERROR`, `SERVER_ERROR`.

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**URL Input:**

```
Format: https://{host}/{path}?{query}
Example: https://api.example.com/v1/items?limit=10
```

**Response Body (`body` field):**

```
kind: string        — "text" or "base64"
content: string     — serialized body content
truncated: boolean  — true if body was cut off at max_response_chars
original_length: number — full byte/character count before truncation
json: any | null    — parsed JSON value if response was valid JSON, otherwise null
```

</details>


## Troubleshooting

<details>
<summary><strong>Invalid URL Format</strong></summary>

- **Cause:** `url` does not start with `http://` or `https://`
- **Solution:**
  1. Provide a full absolute URL (including protocol)
  2. Verify no typos in host/path

</details>

<details>
<summary><strong>Unsupported HTTP Method</strong></summary>

- **Cause:** `method` is outside the allowed set
- **Solution:**
  1. Use one of: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`
  2. Ensure method is passed as a string

</details>

<details>
<summary><strong>Conflicting Body Inputs</strong></summary>

- **Cause:** Both `json_body` and `body` are provided in the same request
- **Solution:**
  1. Use `json_body` for JSON payloads
  2. Use `body` for raw text payloads
  3. Send only one body field per call

</details>

<details>
<summary><strong>Timeout or Upstream Network Errors</strong></summary>

- **Cause:** Slow endpoint, network issues, or unreachable host
- **Solution:**
  1. Increase `timeout_seconds` for long-running endpoints
  2. Confirm the endpoint is publicly reachable
  3. Retry with a reduced payload or simplified query parameters

</details>

<details>
<summary><strong>Response Body Appears Truncated</strong></summary>

- **Cause:** Response size exceeded `max_response_chars`
- **Solution:**
  1. Increase `max_response_chars` if larger output is required
  2. Request smaller payloads with filters/pagination from the upstream API

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[HTTP Methods Reference (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)** — Official method behavior documentation
- **[HTTP Status Codes (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)** — Standard HTTP response status reference
- **[httpx Documentation](https://www.python-httpx.org/)** — Python HTTP client used by this server
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP framework and protocol usage
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>
