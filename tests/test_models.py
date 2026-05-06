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

from io import BytesIO

from wes_api_client.models.run_request import RunRequest
from wes_api_client.models.run_request_tags import RunRequestTags
from wes_api_client.models.run_request_workflow_params import RunRequestWorkflowParams
from wes_api_client.models.run_workflow_body import RunWorkflowBody
from wes_api_client.models.service import Service
from wes_api_client.types import File


def test_run_workflow_body_builds_multipart_parts() -> None:
    payload = BytesIO(b"cwl-version: v1.2")
    attachment = File(
        payload=payload,
        file_name="workflow.cwl",
        mime_type="text/plain",
    )
    body = RunWorkflowBody(
        workflow_params='{"message": "hello"}',
        workflow_type="CWL",
        workflow_type_version="v1.2",
        workflow_url="workflow.cwl",
        workflow_attachment=[attachment],
    )
    body["implementation"] = "test-suite"

    parts = body.to_multipart()

    assert (
        "workflow_type",
        (None, b"CWL", "text/plain"),
    ) in parts
    assert (
        "workflow_type_version",
        (None, b"v1.2", "text/plain"),
    ) in parts
    assert (
        "workflow_url",
        (None, b"workflow.cwl", "text/plain"),
    ) in parts
    assert (
        "implementation",
        (None, b"test-suite", "text/plain"),
    ) in parts

    workflow_attachment = [
        part for part in parts if part[0] == "workflow_attachment"
    ][0]
    assert workflow_attachment[1] == ("workflow.cwl", payload, "text/plain")


def test_dynamic_request_models_round_trip_arbitrary_properties() -> None:
    workflow_params = RunRequestWorkflowParams()
    workflow_params["message"] = "hello"
    workflow_params["output_file"] = "hello.txt"

    tags = RunRequestTags()
    tags["project"] = "unit-tests"

    request = RunRequest(
        workflow_type="CWL",
        workflow_type_version="v1.2",
        workflow_url="workflow.cwl",
        workflow_params=workflow_params,
        tags=tags,
    )
    request["service_extension"] = {"priority": "normal"}

    as_dict = request.to_dict()
    parsed = RunRequest.from_dict(as_dict)

    assert as_dict["workflow_params"] == {
        "message": "hello",
        "output_file": "hello.txt",
    }
    assert as_dict["tags"] == {"project": "unit-tests"}
    assert parsed.workflow_params["message"] == "hello"
    assert parsed.tags["project"] == "unit-tests"
    assert parsed["service_extension"] == {"priority": "normal"}


def test_service_model_parses_dates_camel_case_fields_and_extra_properties() -> None:
    service = Service.from_dict(
        {
            "id": "org.eoepca.wes",
            "name": "EOEPCA WES",
            "type": {
                "group": "org.ga4gh",
                "artifact": "wes",
                "version": "1.1.0",
            },
            "organization": {
                "name": "EOEPCA",
                "url": "https://example.org",
            },
            "version": "1.0.0",
            "contactUrl": "mailto:support@example.org",
            "documentationUrl": "https://docs.example.org",
            "createdAt": "2026-05-06T12:34:56Z",
            "updatedAt": "2026-05-06T13:00:00Z",
            "environment": "test",
            "deployment": "integration",
        }
    )

    as_dict = service.to_dict()

    assert service.contact_url == "mailto:support@example.org"
    assert service.documentation_url == "https://docs.example.org"
    assert service.created_at.year == 2026
    assert service["deployment"] == "integration"
    assert as_dict["contactUrl"] == "mailto:support@example.org"
    assert as_dict["documentationUrl"] == "https://docs.example.org"
    assert as_dict["createdAt"] == "2026-05-06T12:34:56+00:00"
    assert as_dict["deployment"] == "integration"
