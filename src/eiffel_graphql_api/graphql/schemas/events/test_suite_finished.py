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
import graphene
from ..base import EiffelObjectType
from ..lib.generic import json_schema_to_graphql, load


class TestSuiteFinished(EiffelObjectType):
    data = json_schema_to_graphql(
        "TestSuiteFinishedData",
        load("EiffelTestSuiteFinishedEvent.json").get("data").get("properties"),
        override_name={
            "persistentLogs": "testSuitePersistentLogs",
            "outcome": "testSuiteOutcome"
        }
    )
    mongo = None

    def __init__(self, mongo):
        self.mongo = mongo


class TestSuiteFinishedConnection(graphene.Connection):
    class Meta:
        node = TestSuiteFinished
