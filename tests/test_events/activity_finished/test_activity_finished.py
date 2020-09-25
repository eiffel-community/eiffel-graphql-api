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
"""Activity finished tests."""
import logging
from unittest import TestCase

from tests.lib.query_handler import GraphQLQueryHandler

# pylint:disable=wildcard-import,unused-wildcard-import
from .event import *
from .queries import *


logging.basicConfig(level=logging.DEBUG)


class TestActivityFinished(TestCase):
    """Tests for getting activity finished from graphql API."""

    @classmethod
    def setUpClass(cls):
        cls.query_handler = GraphQLQueryHandler("http://127.0.0.1:12345/graphql")
        cls.events = [
            eiffel_activity_triggered_event(),
            eiffel_activity_finished_event(),
        ]
        cls.logger = logging.getLogger("TestActivityFinished")

    def setUp(self):
        self.logger.info("\n")
        for event in self.events:
            insert(event)

    def tearDown(self):
        for event in self.events:
            remove(event)

    def test_activity_finished_execution_uri(self):
        """Test that it is possible to query 'data.outcome' from activity finished.

        Approval criteria:
            - It shall be possible to query 'data.outcome' from graphql.
            - Outcome shall be:
                - {"conclusion": "SUCCESSFUL",
                   "description": "This activity finished successfully."}

        Test steps:
            1. Query 'data.activityOutcome' from ActivityFinished in Graphql.
            2. Verify that the response is correct.
        """
        self.logger.info(
            "STEP: Query 'data.activityOutcome' from ActivityFinished in Graphql."
        )
        self.logger.debug(DATA_ONLY)
        response = self.query_handler.execute(DATA_ONLY)
        self.logger.debug(pretty(response))
        self.logger.info("STEP: Verify that the response is correct.")
        data = self.query_handler.get_node(response, "data")
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)
        self.assertDictEqual(
            data.get("activityOutcome"),
            {
                "conclusion": "SUCCESSFUL",
                "description": "This activity finished successfully.",
            },
        )

    def test_activity_finished_persistent_logs(self):
        """Test that it is possible to query 'data.persistentLogs' from activity finished.

        Approval criteria:
            - It shall be possible to query 'data.persistentLogs' from graphql.
            - Data returned shall be:
                - [ { "uri": "http://log.se", "name": "log"},
                    { "uri": "http://log2.se", "name": "log2"} ]

        Test steps:
            1. Query 'data.activityPersistentLogs' from ActivityFinished in Graphql.
            2. Verify that the response is correct.
        """
        self.logger.info(
            "STEP: Query 'data.activityPersistentLogs' from ActivityFinished in Graphql."
        )
        self.logger.debug(DATA_ONLY)
        response = self.query_handler.execute(DATA_ONLY)
        self.logger.debug(pretty(response))
        self.logger.info("STEP: Verify that the response is correct.")
        data = self.query_handler.get_node(response, "data")
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)
        self.assertEqual(len(data.get("activityPersistentLogs", [])), 2)
        for name, uri in (("log", "http://log.se"), ("log2", "http://log2.se")):
            for log in data.get("activityPersistentLogs"):
                if log.get("name") == name:
                    self.assertEqual(log.get("uri"), uri)
                    break
            else:
                raise AssertionError(
                    "{{'name': {}, 'uri': {}}} not in liveLogs: {}".format(
                        name, uri, data.get("activityPersistentLogs")
                    )
                )

    def test_activity_finished_link(self):
        """Test that it is possible to query a valid activity execution link on activity finished.

        Approval criteria:
            - Graphql shall return an ActivityTriggered event when requesting ActivityExecution.

        Test steps:
            1. Query 'links.ActivityExecution' from ActivityFinished in Graphql.
            2. Verify that the returned event is an ActivityTriggered.
        """
        self.logger.info(
            "STEP: Query 'links.ActivityExecution' from ActivityFinished in Graphql."
        )
        self.logger.debug(LINKS_ONLY)
        response = self.query_handler.execute(LINKS_ONLY)
        self.logger.debug(pretty(response))

        self.logger.info(
            "STEP: Verify that the returned event is an ActivityTriggered."
        )
        link_meta = self.query_handler.get_node(response, "meta")
        self.assertDictEqual(
            link_meta,
            {
                "id": "693c3bac-10a6-4b77-82d7-430139195c1e",
                "type": "EiffelActivityTriggeredEvent",
            },
        )

    def test_activity_finished_meta(self):
        """Test that it is possible to query 'meta' from activity finished.

        Approval criteria:
            - It shall be possible to query 'meta' from graphql.
            - Data returned shall be correct:
                - version: "3.0.0"
                - type   : "EiffelActivityFinishedEvent"
                - id     : "bc73b474-4f5c-4931-b7d5-8588d0a6534a"
                - time   : 1575965387254

        Test steps:
            1. Query 'meta' from  ActivityFinished in Graphql.
            2. Verify that the response is not empty.
            3. Verify that meta data returned correctly.
        """
        self.logger.info("STEP: Query 'meta' from ActivityFinished in Graphql.")
        self.logger.debug(META_ONLY)
        response = self.query_handler.execute(META_ONLY)
        self.logger.debug(pretty(response))

        self.logger.info("STEP: Verify that response is not empty.")
        meta = self.query_handler.get_node(response, "meta")
        self.assertIsInstance(meta, dict)
        self.assertGreater(len(meta), 0)

        self.logger.info("STEP: Verify that meta data returned correctly.")
        self.assertEqual(meta.get("version"), "3.0.0")
        self.assertEqual(meta.get("type"), "EiffelActivityFinishedEvent")
        self.assertEqual(meta.get("id"), "bc73b474-4f5c-4931-b7d5-8588d0a6534a")
        self.assertEqual(meta.get("time"), 1575965387254)
