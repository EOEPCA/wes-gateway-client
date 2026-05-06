# Models

The generated model classes live under `wes_api_client.models`. They are attrs
classes with `to_dict()` and `from_dict()` helpers. Most models also preserve
unknown JSON fields in `additional_properties`.

## Core response models

| Model | Purpose | Key fields |
| --- | --- | --- |
| `ServiceInfo` | WES service metadata and advertised capabilities. | `id`, `name`, `type_`, `organization`, `version`, `workflow_type_versions`, `supported_wes_versions`, `supported_filesystem_protocols`, `workflow_engine_versions`, `auth_instructions_url`, `tags` |
| `RunId` | Identifier returned by submission and cancellation endpoints. | `run_id` |
| `RunStatus` | Lightweight state for one workflow run. | `run_id`, `state` |
| `RunListResponse` | Paginated list of runs. | `runs`, `next_page_token` |
| `RunSummary` | Summary item in a run list. | `run_id`, `tags`, `state`, `start_time`, `end_time` |
| `RunLog` | Detailed workflow run information. | `run_id`, `request`, `state`, `run_log`, `task_logs_url`, `task_logs`, `outputs` |
| `TaskListResponse` | Paginated list of task logs for one run. | `task_logs`, `next_page_token` |
| `TaskLog` | Detailed task log entry. | `id`, `name` and additional log fields returned by the service |
| `ErrorResponse` | Documented WES error response. | `msg`, `status_code` |

## Request models

| Model | Purpose | Key fields |
| --- | --- | --- |
| `RunWorkflowBody` | Multipart body used by `run_workflow`. | `workflow_type`, `workflow_type_version`, `workflow_url`, `workflow_params`, `tags`, `workflow_engine`, `workflow_engine_version`, `workflow_engine_parameters`, `workflow_attachment` |
| `RunRequest` | JSON representation of the request echoed in `RunLog`. | `workflow_type`, `workflow_type_version`, `workflow_url`, `workflow_params`, `tags`, `workflow_engine_parameters`, `workflow_engine`, `workflow_engine_version` |
| `RunRequestWorkflowParams` | Arbitrary workflow input and output parameters. | `additional_properties` |
| `RunRequestTags` | Arbitrary run tags. | `additional_properties` |
| `RunRequestWorkflowEngineParameters` | Arbitrary engine parameters. | `additional_properties` |

## Service capability models

| Model | Purpose |
| --- | --- |
| `ServiceType` | GA4GH service type fields: `group`, `artifact`, `version`. |
| `ServiceOrganization` | Organization metadata for the service provider. |
| `DefaultWorkflowEngineParameter` | Engine parameter name, default value, and type. |
| `WorkflowTypeVersion` | Supported workflow descriptor version. |
| `WorkflowEngineVersion` | Supported workflow engine version. |
| `ServiceInfoWorkflowTypeVersions` | Mapping of workflow type names to supported versions. |
| `ServiceInfoWorkflowEngineVersions` | Mapping of workflow engine names to supported versions. |
| `ServiceInfoSystemStateCounts` | Mapping of WES states to counts. |
| `ServiceInfoTags` | Service-specific metadata tags. |

## State

`State` is a string enum:

| Value | Meaning |
| --- | --- |
| `UNKNOWN` | The state is unknown. |
| `QUEUED` | The run or task is queued. |
| `INITIALIZING` | A worker is preparing to run. |
| `RUNNING` | Execution is in progress. |
| `PAUSED` | Execution is paused. |
| `COMPLETE` | Execution completed successfully. |
| `EXECUTOR_ERROR` | A workflow executor failed. |
| `SYSTEM_ERROR` | The execution system failed outside an executor process. |
| `CANCELED` | The user canceled the run or task. |
| `CANCELING` | Cancellation is in progress. |
| `PREEMPTED` | The system stopped the run or task. |

## Dynamic fields

Dictionary-like models use `additional_properties` and support item access:

```python
from wes_api_client.models.run_request_tags import RunRequestTags

tags = RunRequestTags()
tags["project"] = "demo"
tags["owner"] = "alice"

print(tags.to_dict())
```

Unknown fields from a server response are also retained:

```python
model = ErrorResponse.from_dict(
    {
        "status_code": 500,
        "msg": "internal error",
        "trace_id": "abc123",
    }
)

print(model["trace_id"])
print(model.additional_keys)
```
