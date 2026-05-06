# Workflow Run API

The generated endpoint modules live under `wes_api_client.api`.

## Service information

| Operation | HTTP | Path | Module | Success model | Error statuses |
| --- | --- | --- | --- | --- | --- |
| `GetServiceInfo` | `GET` | `/service-info` | `service_info.get_service_info` | `ServiceInfo` | `400`, `401`, `403`, `500` |

Example:

```python
from wes_api_client.api.service_info import get_service_info

service_info = get_service_info.sync(client=client)
```

## Workflow runs

| Operation | HTTP | Path | Module | Parameters | Success model | Error statuses |
| --- | --- | --- | --- | --- | --- | --- |
| `ListRuns` | `GET` | `/runs` | `workflow_runs.list_runs` | `page_size`, `page_token` | `RunListResponse` | `400`, `401`, `403`, `500` |
| `RunWorkflow` | `POST` | `/runs` | `workflow_runs.run_workflow` | `body` | `RunId` | `400`, `401`, `403`, `500` |
| `GetRunLog` | `GET` | `/runs/{run_id}` | `workflow_runs.get_run_log` | `run_id` | `RunLog` | `401`, `403`, `404`, `500` |
| `GetRunStatus` | `GET` | `/runs/{run_id}/status` | `workflow_runs.get_run_status` | `run_id` | `RunStatus` | `401`, `403`, `404`, `500` |
| `ListTasks` | `GET` | `/runs/{run_id}/tasks` | `workflow_runs.list_tasks` | `run_id`, `page_size`, `page_token` | `TaskListResponse` | `401`, `403`, `404`, `500` |
| `GetTask` | `GET` | `/runs/{run_id}/tasks/{task_id}` | `workflow_runs.get_task` | `run_id`, `task_id` | `TaskLog` | `401`, `403`, `404`, `500` |
| `CancelRun` | `POST` | `/runs/{run_id}/cancel` | `workflow_runs.cancel_run` | `run_id` | `RunId` | `401`, `403`, `404`, `500` |

## Function signatures

```python
get_service_info.sync(*, client)

list_runs.sync(*, client, page_size=UNSET, page_token=UNSET)

run_workflow.sync(*, client, body=UNSET)

get_run_log.sync(run_id, *, client)

get_run_status.sync(run_id, *, client)

list_tasks.sync(run_id, *, client, page_size=UNSET, page_token=UNSET)

get_task.sync(run_id, task_id, *, client)

cancel_run.sync(run_id, *, client)
```

The async variants use the same arguments:

```python
await get_run_status.asyncio(run_id, client=client)
```

## Pagination

`list_runs` and `list_tasks` accept:

| Parameter | Type | Description |
| --- | --- | --- |
| `page_size` | `int | Unset` | Preferred number of items in a page. |
| `page_token` | `str | Unset` | Token from the previous response. |

The parsed responses expose `next_page_token`. An empty or missing token means
there is no next page.

## Workflow submission body

`RunWorkflowBody` is sent as multipart form data.

| Field | Type | Description |
| --- | --- | --- |
| `workflow_type` | `str | Unset` | Workflow descriptor type, such as `CWL` or `WDL`. |
| `workflow_type_version` | `str | Unset` | Descriptor version supported by the WES service. |
| `workflow_url` | `str | Unset` | Absolute workflow URL or relative path to an attached workflow file. |
| `workflow_params` | `str | Unset` | JSON-encoded workflow parameters. |
| `tags` | `str | Unset` | JSON-encoded string tags. |
| `workflow_engine` | `str | Unset` | Workflow engine name. |
| `workflow_engine_version` | `str | Unset` | Workflow engine version. |
| `workflow_engine_parameters` | `str | Unset` | JSON-encoded engine parameters. |
| `workflow_attachment` | `list[File] | Unset` | Files uploaded as `workflow_attachment` multipart parts. |

The WES OpenAPI schema requires `workflow_type`, `workflow_type_version`, and
`workflow_url` for the logical run request. The generated multipart body class
represents them as optional Python fields so callers can build partial objects,
but the service can still reject incomplete submissions.
