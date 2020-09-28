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
"""Artifact created events."""
# Used for local imports pylint:disable=unused-import
from tests.lib.events import insert, remove, drop, pretty


def eiffel_artifact_created_event():
    """Eiffel artifact created event."""
    return {
        "meta": {
            "id": "730f8573-cd69-41f5-81ad-d85aebf28d03",
            "time": 1575968228603,
            "type": "EiffelArtifactCreatedEvent",
            "version": "3.0.0",
        },
        "links": [],
        "data": {
            "identity": "pkg:artifact/created/test@1.0.0",
            "fileInformation": [{"name": "a_file.txt", "tags": ["EPIC_TEST_FILE"]}],
            "buildCommand": "pytest",
            "requiresImplementation": "ANY",
            "implements": ["pkg:composition/link/test@1.0.0"],
            "dependsOn": ["pkg:environment/link/test@1.0.0"],
            "name": "TestingArtifact",
        },
    }


def eiffel_artifact_created_event_composition_link():
    """Eiffel artifact created event with a composition link."""
    return {
        "meta": {
            "id": "c916d139-a54d-4986-b459-6de90f9a9ab2",
            "time": 1575968217533,
            "type": "EiffelArtifactCreatedEvent",
            "version": "3.0.0",
        },
        "links": [
            {"type": "COMPOSITION", "target": "460ff165-125d-468f-a5d2-677d5a939507"}
        ],
        "data": {
            "identity": "pkg:composition/link/test@1.0.0",
        },
    }


def eiffel_artifact_created_event_environment_link():
    """Eiffel artifact created event with an environment link."""
    return {
        "meta": {
            "id": "7f378263-5b9c-4b2a-94dd-cb12f416de28",
            "time": 1575968189735,
            "type": "EiffelArtifactCreatedEvent",
            "version": "3.0.0",
        },
        "links": [
            {"type": "ENVIRONMENT", "target": "0639dc49-8f4f-4732-899e-3aefc66a5bfb"}
        ],
        "data": {
            "identity": "pkg:environment/link/test@1.0.0",
        },
    }


def eiffel_artifact_created_event_previous_version_link():
    """Eiffel artifact created event with a previous version link."""
    return {
        "meta": {
            "id": "ac21cb12-1ddf-4860-b6ac-ca5cab5c7555",
            "time": 1575968326113,
            "type": "EiffelArtifactCreatedEvent",
            "version": "3.0.0",
        },
        "links": [
            {
                "type": "PREVIOUS_VERSION",
                "target": "730f8573-cd69-41f5-81ad-d85aebf28d03",
            }
        ],
        "data": {"identity": "pkg:previous_version/link/test@1.0.0"},
    }


def eiffel_composition_defined():
    """Eiffel composition defined used for link testing."""
    return {
        "meta": {
            "id": "460ff165-125d-468f-a5d2-677d5a939507",
            "time": 1575968096485,
            "type": "EiffelCompositionDefinedEvent",
            "version": "3.0.0",
        },
        "links": [],
        "data": {"name": "Test composition for EiffelDB"},
    }


def eiffel_environment_defined():
    """Eiffel environment defined used for link testing."""
    return {
        "meta": {
            "id": "0639dc49-8f4f-4732-899e-3aefc66a5bfb",
            "time": 1575968122385,
            "type": "EiffelEnvironmentDefinedEvent",
            "version": "3.0.0",
        },
        "links": [],
        "data": {"name": "Test environment for EiffelDB"},
    }
