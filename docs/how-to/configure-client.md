# Configure a Client

Use `Client` for anonymous endpoints and `AuthenticatedClient` for WES services
that expect an authorization header.

## Connect without authentication

```python
from wes_api_client import Client

client = Client(base_url="https://wes.example.org/ga4gh/wes/v1")
```

## Connect with a bearer token

```python
from wes_api_client import AuthenticatedClient

client = AuthenticatedClient(
    base_url="https://wes.example.org/ga4gh/wes/v1",
    token="replace-with-access-token",
)
```

`AuthenticatedClient` writes an `Authorization` header when it constructs the
underlying `httpx.Client` or `httpx.AsyncClient`. The default prefix is
`Bearer`.

## Use a different authentication header

```python
from wes_api_client import AuthenticatedClient

client = AuthenticatedClient(
    base_url="https://wes.example.org/ga4gh/wes/v1",
    token="replace-with-token",
    prefix="",
    auth_header_name="X-Auth-Token",
)
```

## Add headers, cookies, and timeouts

```python
import httpx

from wes_api_client import AuthenticatedClient

client = AuthenticatedClient(
    base_url="https://wes.example.org/ga4gh/wes/v1",
    token="replace-with-access-token",
    headers={"X-Request-Source": "notebook"},
    cookies={"session": "abc123"},
    timeout=httpx.Timeout(30.0),
    follow_redirects=True,
)
```

You can also derive an updated client:

```python
client = client.with_headers({"X-Correlation-ID": "run-2026-05-06"})
client = client.with_timeout(httpx.Timeout(60.0))
```

## Raise on undocumented statuses

By default, documented WES error responses are parsed into `ErrorResponse`, and
undocumented statuses return `None`. To raise an exception for undocumented
statuses, set `raise_on_unexpected_status=True`.

```python
from wes_api_client import AuthenticatedClient
from wes_api_client.errors import UnexpectedStatus

client = AuthenticatedClient(
    base_url="https://wes.example.org/ga4gh/wes/v1",
    token="replace-with-access-token",
    raise_on_unexpected_status=True,
)

try:
    ...
except UnexpectedStatus as exc:
    print(exc.status_code)
    print(exc.content.decode(errors="ignore"))
```

## Use a context manager

The client owns an underlying `httpx` client. Use a context manager when you want
connections closed deterministically.

```python
from wes_api_client import AuthenticatedClient
from wes_api_client.api.service_info import get_service_info

with AuthenticatedClient(
    base_url="https://wes.example.org/ga4gh/wes/v1",
    token="replace-with-access-token",
) as client:
    service_info = get_service_info.sync(client=client)
```

## Use the async client

Every endpoint module also exposes `asyncio()` and `asyncio_detailed()`.

```python
from wes_api_client import AuthenticatedClient
from wes_api_client.api.service_info import get_service_info


async def main() -> None:
    async with AuthenticatedClient(
        base_url="https://wes.example.org/ga4gh/wes/v1",
        token="replace-with-access-token",
    ) as client:
        service_info = await get_service_info.asyncio(client=client)
        print(service_info)
```
