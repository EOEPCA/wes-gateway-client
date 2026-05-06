# Client API

The public package exports `Client` and `AuthenticatedClient`.

```python
from wes_api_client import AuthenticatedClient, Client
```

## Client

`Client` stores configuration used to construct an underlying `httpx.Client` or
`httpx.AsyncClient`.

| Parameter | Type | Description |
| --- | --- | --- |
| `base_url` | `str` | Base URL for the WES API. Endpoint modules call relative paths such as `/runs`. |
| `cookies` | `dict[str, str]` | Cookies sent with every request. |
| `headers` | `dict[str, str]` | Headers sent with every request. |
| `timeout` | `httpx.Timeout | None` | Request timeout passed to `httpx`. |
| `verify_ssl` | `str | bool | ssl.SSLContext` | SSL verification setting passed to `httpx`. |
| `follow_redirects` | `bool` | Whether `httpx` follows redirects. Defaults to `False`. |
| `httpx_args` | `dict[str, Any]` | Additional arguments for `httpx.Client` and `httpx.AsyncClient`. |
| `raise_on_unexpected_status` | `bool` | Raise `UnexpectedStatus` for undocumented HTTP statuses. Defaults to `False`. |

### Client methods

| Method | Description |
| --- | --- |
| `with_headers(headers)` | Return an evolved client with merged headers. Existing underlying clients are also updated. |
| `with_cookies(cookies)` | Return an evolved client with merged cookies. Existing underlying clients are also updated. |
| `with_timeout(timeout)` | Return an evolved client with a new timeout. Existing underlying clients are also updated. |
| `get_httpx_client()` | Return or construct the synchronous `httpx.Client`. |
| `set_httpx_client(client)` | Replace the synchronous `httpx.Client`. |
| `get_async_httpx_client()` | Return or construct the asynchronous `httpx.AsyncClient`. |
| `set_async_httpx_client(async_client)` | Replace the asynchronous `httpx.AsyncClient`. |

## AuthenticatedClient

`AuthenticatedClient` has the same client configuration as `Client`, plus
authentication fields.

| Parameter | Type | Description |
| --- | --- | --- |
| `token` | `str` | Authentication token. |
| `prefix` | `str` | Prefix used before the token. Defaults to `Bearer`. Set to `""` to send the raw token. |
| `auth_header_name` | `str` | Header name used for authentication. Defaults to `Authorization`. |

When the underlying `httpx` client is created, the authentication header is
added to the stored headers:

```text
Authorization: Bearer <token>
```

## Endpoint function variants

Every generated endpoint module exposes four public functions.

| Function | Returns | Use when |
| --- | --- | --- |
| `sync()` | Parsed response model, `ErrorResponse`, or `None` | You only need the parsed response. |
| `sync_detailed()` | `types.Response[T]` | You need status code, headers, raw content, and parsed response. |
| `asyncio()` | Parsed response model, `ErrorResponse`, or `None` | You are using `asyncio` and only need the parsed response. |
| `asyncio_detailed()` | `types.Response[T]` | You are using `asyncio` and need response metadata. |

## Response

`wes_api_client.types.Response` contains:

| Attribute | Type | Description |
| --- | --- | --- |
| `status_code` | `HTTPStatus` | HTTP status as a standard-library enum. |
| `content` | `bytes` | Raw response body. |
| `headers` | `MutableMapping[str, str]` | Response headers from `httpx`. |
| `parsed` | `T | None` | Parsed model, parsed `ErrorResponse`, or `None`. |

## Error handling

Documented error statuses are parsed into `ErrorResponse`. Undocumented statuses
return `None` unless the client has `raise_on_unexpected_status=True`.

```python
from wes_api_client.errors import UnexpectedStatus

client = AuthenticatedClient(
    base_url="https://wes.example.org/ga4gh/wes/v1",
    token="replace-with-access-token",
    raise_on_unexpected_status=True,
)

try:
    response = get_service_info.sync_detailed(client=client)
except UnexpectedStatus as exc:
    print(exc.status_code)
```

Request timeouts are raised by `httpx` as `httpx.TimeoutException`.
