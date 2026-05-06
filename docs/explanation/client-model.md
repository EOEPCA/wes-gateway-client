# Client Model and WES Flow

The client mirrors the GA4GH WES API closely. Endpoint modules represent HTTP
operations, model classes represent OpenAPI schemas, and `Client` objects carry
the transport configuration shared by requests.

## Generated endpoint modules

The package groups endpoint functions by OpenAPI tag:

- `wes_api_client.api.service_info.get_service_info`
- `wes_api_client.api.workflow_runs.list_runs`
- `wes_api_client.api.workflow_runs.run_workflow`
- `wes_api_client.api.workflow_runs.get_run_status`
- `wes_api_client.api.workflow_runs.get_run_log`
- `wes_api_client.api.workflow_runs.list_tasks`
- `wes_api_client.api.workflow_runs.get_task`
- `wes_api_client.api.workflow_runs.cancel_run`

This layout makes the Python API predictable: the module name is the WES
operation name converted to snake case, and the public function names indicate
whether the call is synchronous, asynchronous, parsed-only, or detailed.

## Parsed-only and detailed calls

Each endpoint has a parsed-only function and a detailed function.

`sync()` and `asyncio()` are convenient for ordinary application code. They
return the parsed model directly:

```python
status = get_run_status.sync(run_id, client=client)
```

`sync_detailed()` and `asyncio_detailed()` are better for integration layers,
debugging, and audit logs. They return `types.Response`, which includes the raw
HTTP metadata:

```python
response = get_run_status.sync_detailed(run_id, client=client)
print(response.status_code)
print(response.headers)
print(response.parsed)
```

## WES workflow lifecycle

A typical WES client flow is:

1. Read `/service-info` to discover supported workflow types, engine versions,
   filesystem protocols, and authentication instructions.
2. Submit `/runs` with workflow type, version, URL, parameters, optional engine
   selection, optional tags, and optional attachments.
3. Poll `/runs/{run_id}/status` for lightweight state changes.
4. Read `/runs/{run_id}` for detailed logs, outputs, and task information.
5. Use `/runs/{run_id}/tasks` and `/runs/{run_id}/tasks/{task_id}` when the
   service supports paginated task logs.
6. Call `/runs/{run_id}/cancel` when the run should stop.

The client does not hide this flow behind a single high-level object. That keeps
the generated package close to the standard API and lets applications decide how
to poll, retry, log, and handle service-specific behavior.

## Multipart submission and echoed JSON

WES run submission is multipart form data. The generated `RunWorkflowBody`
therefore stores submission fields as strings and files:

```python
RunWorkflowBody(
    workflow_type="CWL",
    workflow_type_version="v1.2",
    workflow_url="workflow.cwl",
    workflow_params='{"message": "hello"}',
)
```

Later, a run log can include a `RunRequest` object. That response model is a JSON
representation of what the service accepted. Its `workflow_params`, `tags`, and
`workflow_engine_parameters` fields are dictionary-like generated models rather
than multipart strings.

## Error responses are data

Documented WES errors are part of the OpenAPI contract, so the generated client
parses them into `ErrorResponse` instead of raising exceptions. This allows
application code to handle service-level problems alongside successful models.

Unexpected statuses are different. If `raise_on_unexpected_status` is `False`,
they return `None`; if it is `True`, the endpoint raises
`errors.UnexpectedStatus` with the raw response content.

## Where to add higher-level behavior

Keep reusable polling, retry, and logging policy outside the generated endpoint
modules. The generated code is a thin transport and model layer. Application
helpers can call it, inspect typed models, and implement local policy without
making future OpenAPI regeneration harder to merge.
