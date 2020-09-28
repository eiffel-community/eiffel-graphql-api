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
# -*- coding: utf-8 -*-
"""Test scenario 'follow-my-commit'."""
import logging
from unittest import TestCase

from tests.lib.query_handler import GraphQLQueryHandler

# pylint:disable=wildcard-import,unused-wildcard-import
from .event import *
from .queries import *


logging.basicConfig(level=logging.DEBUG)


class TestFollowMyCommit(TestCase):
    """Test the 'follow-my-commit' scenario."""

    @classmethod
    def setUpClass(cls):
        cls.query_handler = GraphQLQueryHandler("http://127.0.0.1:12345/graphql")
        cls.events = [
            eiffel_source_change_created_event(),
            eiffel_source_change_submitted_event(),
            eiffel_composition_defined_event(),
            eiffel_artifact_created_event(),
            eiffel_artifact_published_event(),
            eiffel_confidence_level_modified_event("readyForIntegration"),
            eiffel_confidence_level_modified_event("IntegrationTests"),
            eiffel_confidence_level_modified_event("Daily"),
            eiffel_confidence_level_modified_event("Stability"),
            eiffel_confidence_level_modified_event("Weekly"),
            eiffel_confidence_level_modified_event("FredrikIsNojd"),
        ]
        cls.logger = logging.getLogger("TestFollowMyCommit")

    def setUp(self):
        self.logger.info("\n")
        for event in self.events:
            insert(event)

    def tearDown(self):
        for event in self.events:
            remove(event)

    def test_follow_my_commit(self):
        """Test that you can follow a commit with the graphql API.

        Approval criteria:
            - GraphQL API shall provide a way to determine the confidence levels of a commit.

        Test steps:
            1. Query a commit ID from GraphQL API.
            2. Verify that it is possible to fetch confidence levels from this commit ID.
        """
        self.logger.info("STEP: Query a commit ID from GraphQL API.")
        response = self.query_handler.execute(FOLLOW_MY_COMMIT)
        nodes = self.query_handler.search_for_node_typename(
            response, "ConfidenceLevelModified"
        )

        self.logger.info(
            "STEP: Cerify that it is possible to fetch confidence levels from this commit ID."
        )

        node_names = []
        for node_name, node in nodes:
            self.assertEqual(node_name, "ConfidenceLevelModified")
            node_names.append(node["data"]["name"])

        for node_name in (
            "readyForIntegration",
            "IntegrationTests",
            "Daily",
            "Stability",
            "Weekly",
            "FredrikIsNojd",
        ):
            self.assertIn(node_name, node_names)
