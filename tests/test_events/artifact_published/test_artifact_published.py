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


class TestArtifactPublished(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.query_handler = GraphQLQueryHandler("http://127.0.0.1:12345/graphql")
        cls.events = [
            eiffel_artifact_created_event(),
            eiffel_artifact_published_event()
        ]
        cls.logger = logging.getLogger("TestArtifactPublished")

    def setUp(self):
        self.logger.info("\n")
        for event in self.events:
            insert(event)

    def tearDown(self):
        for event in self.events:
            remove(event)

    def test_artifact_published_data(self):
        """Test that it is possible to query 'data' from artifact published.

        Approval criteria:
            - It shall be possible to query 'data' from graphql.
            - Data shall be:
                - locations: {"type": "OTHER", "uri": "http://anotherplace.com"}

        Test steps:
            1. Query 'data' from ArtifactPublished in Graphql.
            2. Verify that the response is correct.
        """
        self.logger.info("STEP: Query 'data' from ArtifactPublished in Graphql.")
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
                "locations": [
                    {
                        "type": "OTHER",
                        "uri": "http://anotherplace.com"
                    }
                ]
            }
        )

    def test_artifact_published_artifact_link(self):
        """Test that it is possible to query a valid artifact link on artifact published.

        Approval criteria:
            - Graphql shall return an ArtifactCreated event when requesting Artifact.

        Test steps:
            1. Query 'links.Artifact' from ArtifactPublished in Graphql.
            2. Verify that the returned event is a ArtifactCreated.
        """
        self.logger.info("STEP: Query 'links.Artifact' from ArtifactPublished in Graphql.")
        self.logger.debug(LINKS_ONLY)
        response = self.query_handler.execute(LINKS_ONLY)
        self.logger.debug(pretty(response))

        self.logger.info("STEP: Verify that the returned event is a ArtifactCreated.")
        link_meta = self.query_handler.get_node(response, "meta")
        self.assertDictEqual(link_meta, {"id": "7c2b6c13-8dea-4c99-a337-0490269c374d",
                                         "type": "EiffelArtifactCreatedEvent"})

    def test_artifact_published_meta(self):
        """Test that it is possible to query 'meta' from artifact published.

        Approval criteria:
            - It shall be possible to query 'meta' from graphql.
            - Data returned shall be correct:
                - version: "3.0.0"
                - type   : "EiffelArtifactPublishedEvent"
                - id     : "031c2f9a-92f0-4cac-9320-e0113adafd7d"
                - time   : 1575981255471

        Test steps:
            1. Query 'meta' from  ArtifactPublished in Graphql.
            2. Verify that the response is not empty.
            3. Verify that meta data returned correctly.
        """
        self.logger.info("STEP: Query 'meta' from ArtifactPublished in Graphql.")
        self.logger.debug(META_ONLY)
        response = self.query_handler.execute(META_ONLY)
        self.logger.debug(pretty(response))

        self.logger.info("STEP: Verify that response is not empty.")
        meta = self.query_handler.get_node(response, "meta")
        self.assertIsInstance(meta, dict)
        self.assertGreater(len(meta), 0)

        self.logger.info("STEP: Verify that meta data returned correctly.")
        self.assertEqual(meta.get("version"), "3.0.0")
        self.assertEqual(meta.get("type"), "EiffelArtifactPublishedEvent")
        self.assertEqual(meta.get("id"), "031c2f9a-92f0-4cac-9320-e0113adafd7d")
        self.assertEqual(meta.get("time"), "2019-12-10T13:34:15.471000")
