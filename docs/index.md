# WES API Client

`wes-api-client` is a Python client for the GA4GH Workflow Execution Service
(WES) API. It provides typed request and response models, synchronous and
asynchronous endpoint functions, and optional bearer-token authentication.

The client package is generated from `schemas/openapi.json`, then exposed under
`src/wes_api_client`.

## Documentation map

This documentation follows the [Diataxis documentation framework](https://diataxis.fr/):

- **Tutorials** guide a first successful experience.
- **How-to guides** solve practical tasks you are likely to perform against a WES endpoint.
- **Reference** describes the generated client, endpoint functions, and models.
- **Explanation** describes how the generated client maps to WES concepts.

## Install

Install the package in an environment that has access to this repository:

```bash
pip install .
```

The generated code imports `httpx`, `attrs`, and `python-dateutil`, so those
runtime dependencies must also be available in the environment that imports the
client.

## Minimal example

```python
from wes_api_client import AuthenticatedClient
from wes_api_client.api.service_info import get_service_info
from wes_api_client.models.error_response import ErrorResponse
from wes_api_client.models.service_info import ServiceInfo

client = AuthenticatedClient(
    base_url="https://wes.example.org/ga4gh/wes/v1",
    token="replace-with-access-token",
)

service_info = get_service_info.sync(client=client)

if isinstance(service_info, ServiceInfo):
    print(service_info.name)
elif isinstance(service_info, ErrorResponse):
    print(f"WES returned {service_info.status_code}: {service_info.msg}")
else:
    print("WES returned an undocumented response.")
```

Use `AuthenticatedClient` for secured WES endpoints. Use `Client` only for
endpoints that do not require an authorization header.
