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
"""Announcement published tests."""
import logging
from unittest import TestCase

from tests.lib.query_handler import GraphQLQueryHandler

# pylint:disable=wildcard-import,unused-wildcard-import
from .event import *
from .queries import *


logging.basicConfig(level=logging.DEBUG)


class TestAnnouncementPublished(TestCase):
    """Tests for getting announcement published from graphql API."""

    @classmethod
    def setUpClass(cls):
        cls.query_handler = GraphQLQueryHandler("http://127.0.0.1:12345/graphql")
        cls.events = [eiffel_announcement_published_event()]
        cls.logger = logging.getLogger("TestAnnouncementPublished")

    def setUp(self):
        self.logger.info("\n")
        for event in self.events:
            insert(event)

    def tearDown(self):
        for event in self.events:
            remove(event)

    def test_announcement_published_data(self):
        """Test that it is possible to query 'data' from announcement published.

        Approval criteria:
            - It shall be possible to query 'data' from graphql.
            - Data shall be:
                - heading : "This is a heading"
                - body    : "This is a body"
                - uri     : "http://uri.se"
                - severity: "MINOR"

        Test steps:
            1. Query 'data' from AnnouncementPublished in Graphql.
            2. Verify that the response is correct.
        """
        self.logger.info(
            "STEP: Query 'data.activityOutcome' from AnnouncementPublished in Graphql."
        )
        self.logger.debug(DATA_ONLY)
        response = self.query_handler.execute(DATA_ONLY)
        self.logger.debug(pretty(response))
        self.logger.info("STEP: Verify that the response is correct.")
        data = self.query_handler.get_node(response, "data")
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)
        self.assertDictEqual(
            data,
            {
                "heading": "This is a heading",
                "body": "This is a body",
                "uri": "http://uri.se",
                "severity": "MINOR",
            },
        )

    def test_announcement_published_link(self):
        """Test that it is possible to query a valid activity execution link on announcement.

        Approval criteria:
            - Graphql shall return an AnnouncementPublished event when requesting
              ModifiedAnnouncement.

        Test steps:
            1. Query 'links.ModifiedAnnouncement' from AnnouncementPublished in Graphql.
            2. Verify that the returned event is an AnnouncementPublished.
        """
        event = eiffel_announcement_published_event_link()
        try:
            insert(event)
            self.logger.info(
                "STEP: Query 'links.ActivityExecution' from AnnouncementPublished in Graphql."
            )
            self.logger.debug(LINKS_ONLY)
            response = self.query_handler.execute(LINKS_ONLY)
            self.logger.debug(pretty(response))

            self.logger.info(
                "STEP: Verify that the returned event is an AnnouncementPublished."
            )
            link_meta = self.query_handler.get_node(response, "meta")
            self.assertDictEqual(
                link_meta,
                {
                    "id": "4baf56e6-404a-4132-a28b-9ed782f26293",
                    "type": "EiffelAnnouncementPublishedEvent",
                },
            )
        finally:
            remove(event)

    def test_announcement_published_meta(self):
        """Test that it is possible to query 'meta' from announcement published.

        Approval criteria:
            - It shall be possible to query 'meta' from graphql.
            - Data returned shall be correct:
                - version: "3.0.0"
                - type   : "EiffelAnnouncementPublishedEvent"
                - id     : "4baf56e6-404a-4132-a28b-9ed782f26293"
                - time   : 1575966865708

        Test steps:
            1. Query 'meta' from  AnnouncementPublished in Graphql.
            2. Verify that the response is not empty.
            3. Verify that meta data returned correctly.
        """
        self.logger.info("STEP: Query 'meta' from AnnouncementPublished in Graphql.")
        self.logger.debug(META_ONLY)
        response = self.query_handler.execute(META_ONLY)
        self.logger.debug(pretty(response))

        self.logger.info("STEP: Verify that response is not empty.")
        meta = self.query_handler.get_node(response, "meta")
        self.assertIsInstance(meta, dict)
        self.assertGreater(len(meta), 0)

        self.logger.info("STEP: Verify that meta data returned correctly.")
        self.assertEqual(meta.get("version"), "3.0.0")
        self.assertEqual(meta.get("type"), "EiffelAnnouncementPublishedEvent")
        self.assertEqual(meta.get("id"), "4baf56e6-404a-4132-a28b-9ed782f26293")
        self.assertEqual(meta.get("time"), 1575966865708)
