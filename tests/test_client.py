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

import httpx

from wes_api_client import AuthenticatedClient, Client


def test_client_builds_httpx_client_from_configuration() -> None:
    client = Client(
        base_url="https://wes.example.org/ga4gh/wes/v1",
        cookies={"session": "abc123"},
        headers={"X-Client": "unit-test"},
        timeout=httpx.Timeout(5.0),
        follow_redirects=True,
    )

    httpx_client = client.get_httpx_client()

    try:
        assert str(httpx_client.base_url) == "https://wes.example.org/ga4gh/wes/v1/"
        assert httpx_client.cookies["session"] == "abc123"
        assert httpx_client.headers["X-Client"] == "unit-test"
        assert httpx_client.timeout.connect == 5.0
        assert httpx_client.follow_redirects is True
    finally:
        httpx_client.close()


def test_with_headers_updates_existing_httpx_clients() -> None:
    client = Client(base_url="https://wes.example.org")
    httpx_client = client.get_httpx_client()

    try:
        updated = client.with_headers({"X-Trace-ID": "trace-1"})

        assert updated is not client
        assert updated.get_httpx_client().headers["X-Trace-ID"] == "trace-1"
        assert httpx_client.headers["X-Trace-ID"] == "trace-1"
    finally:
        httpx_client.close()


def test_authenticated_client_adds_default_bearer_header() -> None:
    client = AuthenticatedClient(
        base_url="https://wes.example.org",
        token="secret-token",
    )

    httpx_client = client.get_httpx_client()

    try:
        assert httpx_client.headers["Authorization"] == "Bearer secret-token"
    finally:
        httpx_client.close()


def test_authenticated_client_supports_custom_auth_header() -> None:
    client = AuthenticatedClient(
        base_url="https://wes.example.org",
        token="secret-token",
        prefix="",
        auth_header_name="X-Auth-Token",
    )

    httpx_client = client.get_httpx_client()

    try:
        assert httpx_client.headers["X-Auth-Token"] == "secret-token"
        assert "Authorization" not in httpx_client.headers
    finally:
        httpx_client.close()
