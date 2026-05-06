# Copyright 2026 EOEPCA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections.abc import Callable

import httpx
import pytest

from wes_api_client import Client
from wes_api_client.api.workflow_runs import get_run_status, list_runs, run_workflow
from wes_api_client.errors import UnexpectedStatus
from wes_api_client.models.error_response import ErrorResponse
from wes_api_client.models.run_id import RunId
from wes_api_client.models.run_list_response import RunListResponse
from wes_api_client.models.run_status import RunStatus
from wes_api_client.models.run_workflow_body import RunWorkflowBody
from wes_api_client.models.state import State


def build_mocked_client(
    handler: Callable[[httpx.Request], httpx.Response],
    *,
    raise_on_unexpected_status: bool = False,
) -> Client:
    client = Client(
        base_url="https://wes.example.org/ga4gh/wes/v1",
        raise_on_unexpected_status=raise_on_unexpected_status,
    )
    client.set_httpx_client(
        httpx.Client(
            base_url="https://wes.example.org/ga4gh/wes/v1",
            transport=httpx.MockTransport(handler),
        )
    )
    return client


def test_get_run_status_quotes_run_id_and_parses_success_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.raw_path == b"/ga4gh/wes/v1/runs/run%2Fone/status"
        return httpx.Response(
            200,
            json={"run_id": "run/one", "state": "RUNNING"},
        )

    client = build_mocked_client(handler)

    try:
        status = get_run_status.sync("run/one", client=client)
    finally:
        client.get_httpx_client().close()

    assert isinstance(status, RunStatus)
    assert status.run_id == "run/one"
    assert status.state is State.RUNNING


def test_list_runs_sends_pagination_params_and_parses_page() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.raw_path == b"/ga4gh/wes/v1/runs?page_size=2&page_token=n1"
        return httpx.Response(
            200,
            json={
                "runs": [{"run_id": "run-1", "state": "COMPLETE"}],
                "next_page_token": "",
            },
        )

    client = build_mocked_client(handler)

    try:
        page = list_runs.sync(client=client, page_size=2, page_token="n1")
    finally:
        client.get_httpx_client().close()

    assert isinstance(page, RunListResponse)
    assert page.next_page_token == ""
    assert isinstance(page.runs[0], RunStatus)
    assert page.runs[0].run_id == "run-1"
    assert page.runs[0].state is State.COMPLETE


def test_run_workflow_sends_multipart_body_and_parses_run_id() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        content = request.read()

        assert request.method == "POST"
        assert request.url.raw_path == b"/ga4gh/wes/v1/runs"
        assert "multipart/form-data" in request.headers["content-type"]
        assert b'name="workflow_type"' in content
        assert b"CWL" in content
        assert b'name="workflow_params"' in content
        assert b'{"message": "hello"}' in content
        return httpx.Response(200, json={"run_id": "run-123"})

    client = build_mocked_client(handler)
    body = RunWorkflowBody(
        workflow_type="CWL",
        workflow_type_version="v1.2",
        workflow_url="https://example.org/workflows/hello.cwl",
        workflow_params='{"message": "hello"}',
    )

    try:
        result = run_workflow.sync(client=client, body=body)
    finally:
        client.get_httpx_client().close()

    assert isinstance(result, RunId)
    assert result.run_id == "run-123"


def test_documented_error_status_is_parsed_as_error_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        return httpx.Response(
            400,
            json={"status_code": 400, "msg": "workflow_type is required"},
        )

    client = build_mocked_client(handler)

    try:
        result = run_workflow.sync(client=client)
    finally:
        client.get_httpx_client().close()

    assert isinstance(result, ErrorResponse)
    assert result.status_code == 400
    assert result.msg == "workflow_type is required"


def test_undocumented_status_can_raise_unexpected_status() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        return httpx.Response(418, content=b"teapot")

    client = build_mocked_client(handler, raise_on_unexpected_status=True)

    try:
        with pytest.raises(UnexpectedStatus) as exc_info:
            get_run_status.sync("run-1", client=client)
    finally:
        client.get_httpx_client().close()

    assert exc_info.value.status_code == 418
    assert exc_info.value.content == b"teapot"
