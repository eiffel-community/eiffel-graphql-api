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
"""Activity triggered events."""

# Used for local imports pylint:disable=unused-import
from tests.lib.events import insert, remove, drop, pretty


def eiffel_activity_triggered_event():
    """Eiffel activity triggered event."""
    return {
        "meta": {
            "version": "3.0.0",
            "source": {"name": "eiffel-graphql-api-tests"},
            "type": "EiffelActivityTriggeredEvent",
            "id": "6a1abb6e-2c13-4a82-8fe2-012f8fe7c541",
            "time": 1575895437093,
        },
        "links": [],
        "data": {
            "name": "Activity triggered",
            "categories": ["Testing EiffelDB"],
            "triggers": [
                {"type": "MANUAL", "description": "Eiffel Graphql API test trigger"}
            ],
            "executionType": "MANUAL",
        },
    }


def eiffel_activity_triggered_with_activity_context():
    """Eiffel activity triggered event with an activity as context."""
    return {
        "meta": {
            "version": "3.0.0",
            "source": {"name": "eiffel-graphql-api-tests"},
            "type": "EiffelActivityTriggeredEvent",
            "id": "6c05e143-e5c1-4394-ab5f-cda96694ef01",
            "time": 1575895447541,
        },
        "links": [
            {
                "type": "CONTEXT",
                # :meth:`eiffel_activity_triggered_event`
                "target": "6a1abb6e-2c13-4a82-8fe2-012f8fe7c541",
            }
        ],
        "data": {
            "name": "Activity triggered with activity context",
            "categories": ["Testing EiffelDB"],
            "triggers": [
                {"type": "MANUAL", "description": "Eiffel Graphql API test trigger"}
            ],
            "executionType": "MANUAL",
        },
    }


def eiffel_activity_triggered_with_test_suite_context():
    """Eiffel activity triggered event with a test suite as context."""
    return {
        "meta": {
            "version": "3.0.0",
            "source": {"name": "eiffel-graphql-api-tests"},
            "type": "EiffelActivityTriggeredEvent",
            "id": "415c6056-1272-4c6b-9389-5515029f6ee0",
            "time": 1575895456503,
        },
        "links": [
            {
                "type": "CONTEXT",
                # :meth:`eiffel_test_suite_started_event`
                "target": "1a6ff91b-785b-46a6-85fa-01ca0ef97bb2",
            }
        ],
        "data": {
            "name": "Activity triggered with test suite context",
            "categories": ["Testing EiffelDB"],
            "triggers": [
                {"type": "MANUAL", "description": "Eiffel Graphql API test trigger"}
            ],
            "executionType": "MANUAL",
        },
    }


def eiffel_activity_triggered_with_flow_context():
    """Eiffel activity triggered event with a flow context."""
    return {
        "meta": {
            "version": "3.0.0",
            "source": {"name": "eiffel-graphql-api-tests"},
            "type": "EiffelActivityTriggeredEvent",
            "id": "fe7af559-66a3-4f41-8438-0d862bcf8d6f",
            "time": 1575895464263,
        },
        "links": [
            {
                "type": "FLOW_CONTEXT",
                # :meth:`eiffel_flow_context_defined_event`
                "target": "ae61abda-3c8e-41c4-a272-98c218165897",
            }
        ],
        "data": {
            "name": "Activity triggered with flow context",
            "categories": ["Testing EiffelDB"],
            "triggers": [
                {"type": "MANUAL", "description": "Eiffel Graphql API test trigger"}
            ],
            "executionType": "MANUAL",
        },
    }


def eiffel_activity_triggered_with_cause():
    """Eiffel activity triggered event with a cause link."""
    return {
        "meta": {
            "version": "3.0.0",
            "source": {"name": "eiffel-graphql-api-tests"},
            "type": "EiffelActivityTriggeredEvent",
            "id": "8302c73d-ade0-4002-8f98-e725f424cbd7",
            "time": 1575895471409,
        },
        "links": [
            {
                "type": "CAUSE",
                # :meth:`eiffel_activity_triggered_event`
                "target": "6a1abb6e-2c13-4a82-8fe2-012f8fe7c541",
            }
        ],
        "data": {
            "name": "Activity triggered with cause link",
            "categories": ["Testing EiffelDB"],
            "triggers": [
                {"type": "MANUAL", "description": "Eiffel Graphql API test trigger"}
            ],
            "executionType": "MANUAL",
        },
    }


def eiffel_flow_context_defined_event():
    """Eiffel flow context defined for link testing."""
    return {
        "meta": {
            "version": "3.0.0",
            "source": {"name": "eiffel-graphql-api-tests"},
            "type": "EiffelFlowContextDefinedEvent",
            "id": "ae61abda-3c8e-41c4-a272-98c218165897",
            "time": 1575895479125,
        },
        "links": [],
        "data": {"product": "eiffel-graphql-api", "version": "1.0.0"},
    }


def eiffel_test_suite_started_event():
    """Eiffel test suite started defined for link testing."""
    return {
        "meta": {
            "version": "3.0.0",
            "source": {"name": "eiffel-graphql-api-tests"},
            "type": "EiffelTestSuiteStartedEvent",
            "id": "1a6ff91b-785b-46a6-85fa-01ca0ef97bb2",
            "time": 1575895485761,
        },
        "links": [],
        "data": {
            "name": "Eiffel Graphql API test suite started",
            "categories": ["Testing EiffelDB"],
            "types": ["FUNCTIONAL"],
            "liveLogs": [
                {"name": "ThisIsALog", "uri": "http://127.0.0.1:12345/graphql"}
            ],
        },
    }
