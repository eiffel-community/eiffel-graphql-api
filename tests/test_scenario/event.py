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
"""Scenario events."""
# Used for local imports pylint:disable=unused-import
from tests.lib.events import insert, remove, drop, pretty


def eiffel_source_change_created_event():
    """Eiffel source change created event."""
    return {
        "meta": {
            "version": "3.0.0",
            "source": {"name": "eiffel-graphql-api-tests"},
            "type": "EiffelSourceChangeCreatedEvent",
            "id": "a8cec79b-c668-47c4-9fa1-19724496682f",
            "time": 1574922251250,
        },
        "links": [],
        "data": {
            "author": {"name": "Tobias Persson", "id": "tobiaspn"},
            "gitIdentifier": {"commitId": "c9ea15d2d0d3bcfa2856416be4add5a5919764f4"},
        },
    }


def eiffel_source_change_submitted_event():
    """Eiffel source change submitted event."""
    return {
        "meta": {
            "version": "3.0.0",
            "source": {"name": "eiffel-graphql-api-tests"},
            "type": "EiffelSourceChangeSubmittedEvent",
            "id": "bfce0a8a-4dec-43d6-ac06-4b5067e57f87",
            "time": 1574922251251,
        },
        "links": [{"type": "CHANGE", "target": "a8cec79b-c668-47c4-9fa1-19724496682f"}],
        "data": {"submitter": {"name": "Tobias Persson", "id": "tobiaspn"}},
    }


def eiffel_composition_defined_event():
    """Eiffel composition defined event."""
    return {
        "meta": {
            "version": "3.0.0",
            "source": {"name": "eiffel-graphql-api-tests"},
            "type": "EiffelCompositionDefinedEvent",
            "id": "ce2551fb-c275-4e8c-b370-64915247ca8d",
            "time": 1574922251252,
        },
        "links": [
            {"type": "ELEMENT", "target": "bfce0a8a-4dec-43d6-ac06-4b5067e57f87"}
        ],
        "data": {"name": "Eiffel Graphql API Test"},
    }


def eiffel_artifact_created_event():
    """Eiffel artifact created event."""
    return {
        "meta": {
            "version": "3.0.0",
            "source": {"name": "eiffel-graphql-api-tests"},
            "type": "EiffelArtifactCreatedEvent",
            "id": "2c48516a-24f5-4f9e-b9c7-6fe3457acb95",
            "time": 1574922251255,
        },
        "links": [
            {"type": "COMPOSITION", "target": "ce2551fb-c275-4e8c-b370-64915247ca8d"}
        ],
        "data": {"identity": "pkg:eiffel_graphql_api/testing"},
    }


def eiffel_artifact_published_event():
    """Eiffel artifact published event."""
    return {
        "meta": {
            "version": "3.0.0",
            "source": {"name": "eiffel-graphql-api-tests"},
            "type": "EiffelArtifactPublishedEvent",
            "id": "b29b7ba8-a971-4f1c-878e-3c8182a7d525",
            "time": 1574922251253,
        },
        "links": [
            {"type": "ARTIFACT", "target": "2c48516a-24f5-4f9e-b9c7-6fe3457acb95"}
        ],
        "data": {
            "locations": [{"uri": "http://localhost:12345/graphql", "type": "OTHER"}]
        },
    }


def eiffel_confidence_level_modified_event(name="Eiffel Graphql API Tests"):
    """Eiffel confidence level modified event."""
    return {
        "meta": {
            "version": "3.0.0",
            "source": {"name": "eiffel-graphql-api-tests"},
            "type": "EiffelConfidenceLevelModifiedEvent",
            "id": "c44242ba-5329-4610-9334-2ac70f5134b2",
            "time": 1574922251254,
        },
        "links": [
            {"type": "SUBJECT", "target": "2c48516a-24f5-4f9e-b9c7-6fe3457acb95"}
        ],
        "data": {"name": name, "value": "SUCCESS"},
    }
