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
"""Activity finished events."""
# Used for local imports pylint:disable=unused-import
from tests.lib.events import insert, remove, drop, pretty


def eiffel_activity_finished_event():
    """Eiffel activity finished event."""
    return {
        "meta": {
            "id": "bc73b474-4f5c-4931-b7d5-8588d0a6534a",
            "time": 1575965387254,
            "type": "EiffelActivityFinishedEvent",
            "version": "3.0.0",
        },
        "links": [
            {
                "target": "693c3bac-10a6-4b77-82d7-430139195c1e",
                "type": "ACTIVITY_EXECUTION",
            }
        ],
        "data": {
            "outcome": {
                "conclusion": "SUCCESSFUL",
                "description": "This activity finished successfully.",
            },
            "persistentLogs": [
                {"name": "log", "uri": "http://log.se"},
                {"name": "log2", "uri": "http://log2.se"},
            ],
        },
    }


def eiffel_activity_triggered_event():
    """Eiffel activity triggered event."""
    return {
        "meta": {
            "version": "3.0.0",
            "source": {"name": "eiffel-graphql-api-tests"},
            "type": "EiffelActivityTriggeredEvent",
            "id": "693c3bac-10a6-4b77-82d7-430139195c1e",
            "time": 1575895437093,
        },
        "links": [],
        "data": {
            "name": "Activity triggered",
            "categories": ["Testing EiffelDB Canceled"],
            "triggers": [
                {"type": "MANUAL", "description": "Eiffel Graphql API test trigger"}
            ],
            "executionType": "MANUAL",
        },
    }
