# Monitor Workflow Runs

The workflow run endpoints let you page through runs, poll a run status, fetch
detailed logs, inspect task logs, and cancel a run.

## List runs

```python
from wes_api_client.api.workflow_runs import list_runs
from wes_api_client.models.run_list_response import RunListResponse

page = list_runs.sync(client=client, page_size=20)

if isinstance(page, RunListResponse):
    for run in page.runs or []:
        print(run.to_dict())
```

## Page through all runs

```python
from wes_api_client.api.workflow_runs import list_runs
from wes_api_client.models.run_list_response import RunListResponse

page_token = None

while True:
    page = list_runs.sync(
        client=client,
        page_size=50,
        page_token=page_token,
    )

    if not isinstance(page, RunListResponse):
        break

    for run in page.runs or []:
        print(run.to_dict())

    page_token = page.next_page_token
    if not page_token:
        break
```

## Poll a run until it stops

```python
import time

from wes_api_client.api.workflow_runs import get_run_status
from wes_api_client.models.run_status import RunStatus
from wes_api_client.models.state import State

terminal_states = {
    State.COMPLETE,
    State.EXECUTOR_ERROR,
    State.SYSTEM_ERROR,
    State.CANCELED,
    State.PREEMPTED,
}

while True:
    status = get_run_status.sync("replace-with-run-id", client=client)

    if not isinstance(status, RunStatus):
        print("No status was returned.")
        break

    print(status.state)

    if status.state in terminal_states:
        break

    time.sleep(10)
```

## Fetch a detailed run log

```python
from wes_api_client.api.workflow_runs import get_run_log
from wes_api_client.models.run_log import RunLog

run_log = get_run_log.sync("replace-with-run-id", client=client)

if isinstance(run_log, RunLog):
    print(run_log.state)
    if run_log.run_log:
        print(run_log.run_log.stdout)
        print(run_log.run_log.stderr)
    if run_log.outputs:
        print(run_log.outputs.to_dict())
```

## List tasks for a run

```python
from wes_api_client.api.workflow_runs import list_tasks
from wes_api_client.models.task_list_response import TaskListResponse

tasks = list_tasks.sync("replace-with-run-id", client=client, page_size=100)

if isinstance(tasks, TaskListResponse):
    for task in tasks.task_logs or []:
        print(task.to_dict())
```

## Fetch one task

```python
from wes_api_client.api.workflow_runs import get_task
from wes_api_client.models.task_log import TaskLog

task = get_task.sync(
    "replace-with-run-id",
    "replace-with-task-id",
    client=client,
)

if isinstance(task, TaskLog):
    print(task.name)
    print(task.stdout)
```

## Cancel a run

```python
from wes_api_client.api.workflow_runs import cancel_run
from wes_api_client.models.run_id import RunId

cancelled = cancel_run.sync("replace-with-run-id", client=client)

if isinstance(cancelled, RunId):
    print(f"Cancellation requested for {cancelled.run_id}")
```
