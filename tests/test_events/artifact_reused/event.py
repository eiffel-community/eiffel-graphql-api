# Copyright 2019 Axis Communications AB.
#
# For a full list of individual contributors, please see the commit history.
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
"""Test artifact reused events."""
# Used for local imports pylint:disable=unused-import
from tests.lib.events import insert, remove, drop, pretty


def eiffel_artifact_reused_event():
    """Eiffel artifact reused event."""
    return {
        "meta": {
            "id": "0284875e-4f2f-4589-b6df-797afb039b88",
            "time": 1575985114977,
            "type": "EiffelArtifactReusedEvent",
            "version": "3.0.0",
        },
        "links": [],
        "data": {},
    }


def eiffel_artifact_reused_event_composition_link():
    """Eiffel artifact reused with a composition link."""
    return {
        "meta": {
            "id": "0e5d23cc-e3ed-45e5-9370-9fbcfd260812",
            "time": 1575985132391,
            "type": "EiffelArtifactReusedEvent",
            "version": "3.0.0",
        },
        "links": [
            {"type": "COMPOSITION", "target": "fb2c7a14-1aed-4fcb-9efe-3ff8496d286c"}
        ],
        "data": {},
    }


def eiffel_artifact_reused_event_artifact_reused_link():
    """Eiffel artifact reused with a reused artifact link."""
    return {
        "meta": {
            "id": "88feb145-707c-49df-afdf-c0b80aca9cc3",
            "time": 1575985150183,
            "type": "EiffelArtifactReusedEvent",
            "version": "3.0.0",
        },
        "links": [
            {
                "type": "REUSED_ARTIFACT",
                "target": "bd7cbd8a-1aef-4b4e-87d3-42ffa4acb354",
            }
        ],
        "data": {},
    }


def eiffel_artifact_created_event():
    """Eiffel artifact created event."""
    return {
        "meta": {
            "id": "bd7cbd8a-1aef-4b4e-87d3-42ffa4acb354",
            "time": 1575985169055,
            "type": "EiffelArtifactCreatedEvent",
            "version": "3.0.0",
        },
        "links": [],
        "data": {"identity": "pkg:artifact/created/test@1.0.0"},
    }


def eiffel_composition_defined():
    """Eiffel composition defined event used for link testing."""
    return {
        "meta": {
            "id": "fb2c7a14-1aed-4fcb-9efe-3ff8496d286c",
            "time": 1575985180633,
            "type": "EiffelCompositionDefinedEvent",
            "version": "3.0.0",
        },
        "links": [],
        "data": {"name": "Test composition for EiffelDB"},
    }
