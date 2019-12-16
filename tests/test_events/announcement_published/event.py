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
from tests.lib.events import insert, remove, drop, pretty  # Used for local imports


def eiffel_announcement_published_event():
    return {
        "meta": {
            "id": "4baf56e6-404a-4132-a28b-9ed782f26293",
            "time": 1575966865708,
            "type": "EiffelAnnouncementPublishedEvent",
            "version": "3.0.0"
        },
        "links": [],
        "data": {
            "heading": "This is a heading",
            "body": "This is a body",
            "uri": "http://uri.se",
            "severity": "MINOR"
        }
    }


def eiffel_announcement_published_event_link():
    return {
        "meta": {
            "id": "bc73b474-4f5c-4931-b7d5-8588d0a6534a",
            "time": 1575966867262,
            "type": "EiffelAnnouncementPublishedEvent",
            "version": "3.0.0"
        },
        "links": [
            {
                "type": "MODIFIED_ANNOUNCEMENT",
                "target": "4baf56e6-404a-4132-a28b-9ed782f26293"
            }
        ],
        "data": {
            "heading": "This is a modified heading",
            "body": "This is a modified body",
            "severity": "MAJOR"
        }
    }
