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
"""Artifact published events."""
# Used for local imports pylint:disable=unused-import
from tests.lib.events import insert, remove, drop, pretty


def eiffel_artifact_published_event():
    """Eiffel artifact published event."""
    return {
        "meta": {
            "id": "031c2f9a-92f0-4cac-9320-e0113adafd7d",
            "time": 1575981255471,
            "type": "EiffelArtifactPublishedEvent",
            "version": "3.0.0",
        },
        "links": [
            {"type": "ARTIFACT", "target": "7c2b6c13-8dea-4c99-a337-0490269c374d"}
        ],
        "data": {"locations": [{"type": "OTHER", "uri": "http://anotherplace.com"}]},
    }


def eiffel_artifact_created_event():
    """Eiffel artifact created event."""
    return {
        "meta": {
            "id": "7c2b6c13-8dea-4c99-a337-0490269c374d",
            "time": 1575981274307,
            "type": "EiffelArtifactCreatedEvent",
            "version": "3.0.0",
        },
        "links": [],
        "data": {"identity": "pkg:artifact/created/test@1.0.0"},
    }
