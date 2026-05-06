# Submit Your First Workflow Run

In this tutorial we will create a WES client, read the service information,
submit a simple workflow by URL, and fetch the run status.

You need:

- A WES endpoint base URL, for example `https://wes.example.org/ga4gh/wes/v1`.
- A bearer token for that endpoint.
- A CWL or WDL workflow URL that the WES service can access.

## Create a small script

Create `first_run.py` with the following content:

```python
import json

from wes_api_client import AuthenticatedClient
from wes_api_client.api.service_info import get_service_info
from wes_api_client.api.workflow_runs import get_run_status, run_workflow
from wes_api_client.models.error_response import ErrorResponse
from wes_api_client.models.run_id import RunId
from wes_api_client.models.run_status import RunStatus
from wes_api_client.models.run_workflow_body import RunWorkflowBody
from wes_api_client.models.service_info import ServiceInfo


WES_BASE_URL = "https://wes.example.org/ga4gh/wes/v1"
TOKEN = "replace-with-access-token"


client = AuthenticatedClient(base_url=WES_BASE_URL, token=TOKEN)

service_info = get_service_info.sync(client=client)
if isinstance(service_info, ServiceInfo):
    print(f"Connected to {service_info.name}")
else:
    print("The WES service did not return service information.")
    raise SystemExit(1)

body = RunWorkflowBody(
    workflow_type="CWL",
    workflow_type_version="v1.2",
    workflow_url="https://example.org/workflows/hello.cwl",
    workflow_params=json.dumps(
        {
            "message": "hello from wes-api-client",
            "output_file": "hello.txt",
        }
    ),
    tags=json.dumps({"purpose": "first-run"}),
)

submitted = run_workflow.sync(client=client, body=body)

if isinstance(submitted, ErrorResponse):
    print(f"Run submission failed: {submitted.msg}")
    raise SystemExit(1)

if not isinstance(submitted, RunId):
    print("The WES service returned an undocumented submission response.")
    raise SystemExit(1)

print(f"Submitted run {submitted.run_id}")

status = get_run_status.sync(submitted.run_id, client=client)
if isinstance(status, RunStatus):
    print(f"{status.run_id}: {status.state}")
else:
    print("The WES service did not return a run status.")
```

## Run it

```bash
python first_run.py
```

The output should show the service name, then a run identifier, then the current
state of the run:

```text
Connected to Example WES
Submitted run 7b8e...
7b8e...: QUEUED
```

If the run is already executing, the state may be `INITIALIZING`, `RUNNING`, or
another WES state.

## Notice the shape of the client

The endpoint modules return typed model objects when the server response matches
the OpenAPI contract. In this example:

- `get_service_info.sync()` returns `ServiceInfo`, `ErrorResponse`, or `None`.
- `run_workflow.sync()` returns `RunId`, `ErrorResponse`, or `None`.
- `get_run_status.sync()` returns `RunStatus`, `ErrorResponse`, or `None`.

The `sync()` functions return only the parsed model. The `sync_detailed()`
functions return status code, headers, raw content, and the parsed model.
