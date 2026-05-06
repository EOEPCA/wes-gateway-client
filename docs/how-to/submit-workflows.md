# Submit Workflows

Use `wes_api_client.api.workflow_runs.run_workflow` to submit a workflow to a
WES endpoint. The generated client sends the request as `multipart/form-data`
using `RunWorkflowBody.to_multipart()`.

## Submit a workflow by URL

```python
import json

from wes_api_client import AuthenticatedClient
from wes_api_client.api.workflow_runs import run_workflow
from wes_api_client.models.error_response import ErrorResponse
from wes_api_client.models.run_id import RunId
from wes_api_client.models.run_workflow_body import RunWorkflowBody

client = AuthenticatedClient(
    base_url="https://wes.example.org/ga4gh/wes/v1",
    token="replace-with-access-token",
)

body = RunWorkflowBody(
    workflow_type="CWL",
    workflow_type_version="v1.2",
    workflow_url="https://example.org/workflows/align.cwl",
    workflow_params=json.dumps(
        {
            "reads": "s3://example-bucket/reads.fastq.gz",
            "reference": "s3://example-bucket/reference.fa",
        }
    ),
    tags=json.dumps({"project": "demo", "owner": "alice"}),
)

result = run_workflow.sync(client=client, body=body)

if isinstance(result, RunId):
    print(result.run_id)
elif isinstance(result, ErrorResponse):
    print(f"{result.status_code}: {result.msg}")
```

`workflow_params`, `tags`, and `workflow_engine_parameters` are string fields in
`RunWorkflowBody`, because they are sent as multipart text parts. Use
`json.dumps()` when the WES server expects JSON values in those fields.

## Submit a workflow with an attachment

Use `types.File` for each `workflow_attachment`. When an attached workflow file
is the primary workflow, set `workflow_url` to the attachment filename.

```python
import json

from wes_api_client import AuthenticatedClient
from wes_api_client.api.workflow_runs import run_workflow
from wes_api_client.models.run_workflow_body import RunWorkflowBody
from wes_api_client.types import File

client = AuthenticatedClient(
    base_url="https://wes.example.org/ga4gh/wes/v1",
    token="replace-with-access-token",
)

with open("workflow.cwl", "rb") as workflow_file:
    body = RunWorkflowBody(
        workflow_type="CWL",
        workflow_type_version="v1.2",
        workflow_url="workflow.cwl",
        workflow_params=json.dumps({"message": "hello"}),
        workflow_attachment=[
            File(
                payload=workflow_file,
                file_name="workflow.cwl",
                mime_type="text/plain",
            )
        ],
    )

    result = run_workflow.sync(client=client, body=body)

print(result)
```

Keep the file object open until `run_workflow.sync()` returns. The generated
client hands the file object to `httpx` when it builds the multipart request.

## Select a workflow engine

Some WES services support more than one workflow engine. Use service information
to discover what the endpoint advertises, then provide `workflow_engine` and
`workflow_engine_version` when needed.

```python
import json

from wes_api_client.models.run_workflow_body import RunWorkflowBody

body = RunWorkflowBody(
    workflow_type="WDL",
    workflow_type_version="1.0",
    workflow_url="https://example.org/workflows/call-cache-demo.wdl",
    workflow_engine="cromwell",
    workflow_engine_version="85",
    workflow_engine_parameters=json.dumps({"workflow_failure_mode": "ContinueWhilePossible"}),
)
```

## Inspect the HTTP response

Use `sync_detailed()` when you need headers, status code, or raw content.

```python
from wes_api_client.api.workflow_runs import run_workflow

response = run_workflow.sync_detailed(client=client, body=body)

print(response.status_code)
print(response.headers.get("x-request-id"))
print(response.parsed)
```
