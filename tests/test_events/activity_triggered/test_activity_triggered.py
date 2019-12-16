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
import pytest
import logging
from unittest import TestCase
from .event import *
from .queries import *
from tests.lib.query_handler import GraphQLQueryHandler


logging.basicConfig(
    level=logging.DEBUG
)



class TestActivityTriggered(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.query_handler = GraphQLQueryHandler("http://127.0.0.1:12345/graphql")
        cls.events = [eiffel_activity_triggered_event()]
        cls.logger = logging.getLogger("TestActivityTriggered")

    def setUp(self):
        self.logger.info("\n")
        for event in self.events:
            insert(event)

    def tearDown(self):
        for event in self.events:
            remove(event)

    def test_activity_triggered_data_name(self):
        """Test that it is possible to query 'data.name' from activity triggered.

        Approval criteria:
            - It shall be possible to query 'data.name' from graphql.

        Test steps:
            1. Query 'data.name' from ActivityTriggered in Graphql.
            2. Verify that the response is not empty.
        """
        self.logger.info("STEP: Query 'data.name' from ActivityTriggered in Graphql.")
        self.logger.debug(DATA_NAME_ONLY)
        response = self.query_handler.execute(DATA_NAME_ONLY)
        self.logger.debug(pretty(response))
        self.logger.info("STEP: Verify that the response is not empty.")
        data = self.query_handler.get_node(response, "data")
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)

    def test_activity_triggered_data_categories(self):
        """Test that it is possible to query 'data' from activity triggered.

        Approval criteria:
            - It shall be possible to query 'data' from graphql.
            - Data returned shall be correct:
                - name             : "Activity triggered"
                - categories       : [{"type": "Testing EiffelDB"}]
                - activityTriggers : [{"type": "MANUAL", "description": "Eiffel Graphql API test trigger"}]
                - executionType    : "MANUAL"

        Test steps:
            1. Query all data from ActivityTriggered in Graphql.
            2. Verify that the response is not empty.
            3. Verify that data returned correctly.
        """
        self.logger.info("STEP: Query all data from ActivityTriggered in Graphql.")
        self.logger.debug(DATA_ONLY)
        response = self.query_handler.execute(DATA_ONLY)
        self.logger.debug(pretty(response))

        self.logger.info("STEP: Verify that the response is not empty.")
        data = self.query_handler.get_node(response, "data")
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)

        self.logger.info("STEP: Verify that data returned correctly.")
        self.assertEqual(data.get("categories"), [{"type": "Testing EiffelDB"}])
        self.assertEqual(len(data.get("activityTriggers", [])), 1)
        self.assertDictEqual(data.get("activityTriggers")[0],
                             {"type": "MANUAL", "description": "Eiffel Graphql API test trigger"})
        self.assertEqual(data.get("executionType"), "MANUAL")
        self.assertEqual(data.get("name"), "Activity triggered")

    def test_activity_triggered_meta(self):
        """Test that it is possible to query 'meta' from activity triggered.

        Approval criteria:
            - It shall be possible to query 'meta' from graphql.
            - Data returned shall be correct:
                - version: "3.0.0"
                - type   : "EiffelActivityTriggeredEvent"
                - id     : "6a1abb6e-2c13-4a82-8fe2-012f8fe7c541"
                - time   : 1575895437093

        Test steps:
            1. Query 'meta' from  ActivityTriggered in Graphql.
            2. Verify that the response is not empty.
            3. Verify that meta data returned correctly.
        """
        self.logger.info("STEP: Query 'meta' from ActivityTriggered in Graphql.")
        self.logger.debug(META_ONLY)
        response = self.query_handler.execute(META_ONLY)
        self.logger.debug(pretty(response))

        self.logger.info("STEP: Verify that response is not empty.")
        meta = self.query_handler.get_node(response, "meta")
        self.assertIsInstance(meta, dict)
        self.assertGreater(len(meta), 0)

        self.logger.info("STEP: Verify that meta data returned correctly.")
        self.assertEqual(meta.get("version"), "3.0.0")
        self.assertEqual(meta.get("type"), "EiffelActivityTriggeredEvent")
        self.assertEqual(meta.get("id"), "6a1abb6e-2c13-4a82-8fe2-012f8fe7c541")
        self.assertEqual(meta.get("time"), "2019-12-09T13:43:57.093000")

    def test_activity_triggered_links(self):
        """Test that it is possible to query 'links' from activity triggered.

        Approval criteria:
            - It shall be possible to query 'links' from graphql.

        Test steps:
            1. Query 'links' from ActivityTriggered in Graphql.
            2. Verify that the 'links' key exists.
        """
        self.logger.info("STEP: Query 'links' from ActivityTriggered in Graphql.")
        self.logger.debug(LINKS_ONLY)
        response = self.query_handler.execute(LINKS_ONLY)
        self.logger.debug(pretty(response))

        self.logger.info("STEP: Verify that the 'links' key exists.")
        links = self.query_handler.get_node(response, "links")
        self.assertIsInstance(links, list)
        self.assertEqual(links, [])

    def test_activity_triggered_context_link(self):
        """Test that it is possible to query 'links.context' from activity triggered.

        Approval criteria:
            - It shall be possible to query an empty 'links.context' from graphql.

        Test steps:
            1. Query 'links.context' from ActivityTriggered in Graphql.
            2. Verify that the 'links' key exists.
        """
        self.logger.info("STEP: Query 'links.context' from ActivityTriggered in Graphql.")
        self.logger.debug(CONTEXT_LINK)
        response = self.query_handler.execute(CONTEXT_LINK)
        self.logger.debug(pretty(response))

        self.logger.info("STEP: Verify that the 'links' key exists.")
        links = self.query_handler.get_node(response, "links")
        self.assertIsInstance(links, list)
        self.assertEqual(links, [])

    def test_activity_triggered_context_link_to_activity_triggered(self):
        """Test that it is possible to query a valid context link on activity triggered.

        Approval criteria:
            - Graphql shall return an ActivityTriggered event when requesting Context.

        Test steps:
            1. Query 'links.Context.ActivityTriggered' from ActivityTriggered in Graphql.
            2. Verify that the returned event is an ActivityTriggered.
        """
        event = eiffel_activity_triggered_with_activity_context()
        try:
            insert(event)
            self.logger.info("STEP: Query 'links.Context.ActivityTriggered' from ActivityTriggered in Graphql.")
            self.logger.debug(CONTEXT_LINK_TO_ACTIVITY_TRIGGERED)
            response = self.query_handler.execute(CONTEXT_LINK_TO_ACTIVITY_TRIGGERED)
            self.logger.debug(pretty(response))

            self.logger.info("STEP: Verify that the returned event is an ActivityTriggered.")
            link_meta = self.query_handler.get_node(response, "meta")
            self.assertDictEqual(link_meta, {"id": "6a1abb6e-2c13-4a82-8fe2-012f8fe7c541",
                                             "type": "EiffelActivityTriggeredEvent"})
        finally:
            remove(event)

    def test_activity_triggered_context_link_to_test_suite(self):
        """Test that it is possible to query a valid context link on activity triggered.

        Approval criteria:
            - Graphql shall return a TestSuiteStarted event when requesting Context.

        Test steps:
            1. Query 'links.Context.TestSuiteStarted' from ActivityTriggered in Graphql.
            2. Verify that the returned event is a TestSuiteStarted.
        """
        events = [eiffel_test_suite_started_event(),
                  eiffel_activity_triggered_with_test_suite_context()]
        try:
            insert(events)
            self.logger.info("STEP: Query 'links.Context.TestSuiteStarted' from ActivityTriggered in Graphql.")
            self.logger.debug(CONTEXT_LINK_TO_TEST_SUITE_STARTED)
            response = self.query_handler.execute(CONTEXT_LINK_TO_TEST_SUITE_STARTED)
            self.logger.debug(pretty(response))

            self.logger.info("STEP: Verify that the returned event is a TestSuiteStarted.")
            link_meta = self.query_handler.get_node(response, "meta")
            self.assertDictEqual(link_meta, {"id": "1a6ff91b-785b-46a6-85fa-01ca0ef97bb2",
                                             "type": "EiffelTestSuiteStartedEvent"})
        finally:
            remove(events)

    def test_activity_triggered_cause_link(self):
        """Test that it is possible to query a valid cause link on activity triggered.

        Approval criteria:
            - Graphql shall return an ActivityTriggered event when requesting Cause.

        Test steps:
            1. Query 'links.Cause.ActivityTriggered' from ActivityTriggered in Graphql.
            2. Verify that the returned event is an ActivityTriggered.
        """
        event = eiffel_activity_triggered_with_cause()
        try:
            insert(event)
            self.logger.info("STEP: Query 'links.Cause.TestSuiteStarted' from ActivityTriggered in Graphql.")
            self.logger.debug(CAUSE_LINK)
            response = self.query_handler.execute(CAUSE_LINK)
            self.logger.debug(pretty(response))

            self.logger.info("STEP: Verify that the returned event is an ActivityTriggered.")
            link_meta = self.query_handler.get_node(response, "meta")
            self.assertDictEqual(link_meta, {"id": "6a1abb6e-2c13-4a82-8fe2-012f8fe7c541",
                                             "type": "EiffelActivityTriggeredEvent"})
        finally:
            remove(event)

    def test_activity_triggered_flow_context(self):
        """Test that it is possible to query a valid flow context link on activity triggered.

        Approval criteria:
            - Graphql shall return an ActivityTriggered event when requesting FlowContext.

        Test steps:
            1. Query 'links.FlowContext.FlowContextDefined' from ActivityTriggered in Graphql.
            2. Verify that the returned event is a FlowContextDefined.
        """
        events = [eiffel_flow_context_defined_event(),
                  eiffel_activity_triggered_with_flow_context()]
        try:
            insert(events)
            self.logger.info("STEP: Query 'links.FlowContext.FlowContextDefined' from ActivityTriggered in Graphql.")
            self.logger.debug(FLOW_CONTEXT_LINK)
            response = self.query_handler.execute(FLOW_CONTEXT_LINK)
            self.logger.debug(pretty(response))

            self.logger.info("STEP: Verify that the returned event is an FlowContextDefined.")
            link_meta = self.query_handler.get_node(response, "meta")
            self.assertDictEqual(link_meta, {"id": "ae61abda-3c8e-41c4-a272-98c218165897",
                                             "type": "EiffelFlowContextDefinedEvent"})
        finally:
            remove(events)
