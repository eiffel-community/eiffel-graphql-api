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


class TestArtifactReused(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.query_handler = GraphQLQueryHandler("http://127.0.0.1:12345/graphql")
        cls.events = [
            eiffel_artifact_reused_event()
        ]
        cls.logger = logging.getLogger("TestArtifactReused")

    def setUp(self):
        self.logger.info("\n")
        for event in self.events:
            insert(event)

    def tearDown(self):
        for event in self.events:
            remove(event)

    def test_artifact_reused_artifact_link(self):
        """Test that it is possible to query a valid reused artifact link on artifact reused.

        Approval criteria:
            - Graphql shall return an ArtifactCreated event when requesting ReusedArtifact.

        Test steps:
            1. Query 'links.ReusedArtifact' from ArtifactReused in Graphql.
            2. Verify that the returned event is a ArtifactCreated.
        """
        events = [
            eiffel_artifact_created_event(),
            eiffel_artifact_reused_event_artifact_reused_link()
        ]
        try:
            for event in events:
                insert(event)
            self.logger.info("STEP: Query 'links.ReusedArtifact' from ArtifactReused in Graphql.")
            self.logger.debug(LINKS_ARTIFACT)
            response = self.query_handler.execute(LINKS_ARTIFACT)
            self.logger.debug(pretty(response))

            self.logger.info("STEP: Verify that the returned event is a ArtifactCreated.")
            link_meta = self.query_handler.get_node(response, "meta")
            self.assertDictEqual(link_meta, {"id": "bd7cbd8a-1aef-4b4e-87d3-42ffa4acb354",
                                             "type": "EiffelArtifactCreatedEvent"})
        finally:
            for event in events:
                remove(event)

    def test_artifact_reused_composition_link(self):
        """Test that it is possible to query a valid composition link on artifact reused.

        Approval criteria:
            - Graphql shall return an CompositionDefined event when requesting Composition.

        Test steps:
            1. Query 'links.Composition' from ArtifactReused in Graphql.
            2. Verify that the returned event is a CompositionDefined.
        """
        events = [
            eiffel_composition_defined(),
            eiffel_artifact_reused_event_composition_link()
        ]
        try:
            for event in events:
                insert(event)
            self.logger.info("STEP: Query 'links.ReusedArtifact' from ArtifactReused in Graphql.")
            self.logger.debug(LINKS_COMPOSITION)
            response = self.query_handler.execute(LINKS_COMPOSITION)
            self.logger.debug(pretty(response))

            self.logger.info("STEP: Verify that the returned event is a CompositionDefined.")
            link_meta = self.query_handler.get_node(response, "meta")
            self.assertDictEqual(link_meta, {"id": "fb2c7a14-1aed-4fcb-9efe-3ff8496d286c",
                                             "type": "EiffelCompositionDefinedEvent"})
        finally:
            for event in events:
                remove(event)

    def test_artifact_reused_meta(self):
        """Test that it is possible to query 'meta' from artifact reused.

        Approval criteria:
            - It shall be possible to query 'meta' from graphql.
            - Data returned shall be correct:
                - version: "3.0.0"
                - type   : "EiffelArtifactReusedEvent"
                - id     : "0284875e-4f2f-4589-b6df-797afb039b88"
                - time   : 1575985114977

        Test steps:
            1. Query 'meta' from  ArtifactReused in Graphql.
            2. Verify that the response is not empty.
            3. Verify that meta data returned correctly.
        """
        self.logger.info("STEP: Query 'meta' from ArtifactReused in Graphql.")
        self.logger.debug(META_ONLY)
        response = self.query_handler.execute(META_ONLY)
        self.logger.debug(pretty(response))

        self.logger.info("STEP: Verify that response is not empty.")
        meta = self.query_handler.get_node(response, "meta")
        self.assertIsInstance(meta, dict)
        self.assertGreater(len(meta), 0)

        self.logger.info("STEP: Verify that meta data returned correctly.")
        self.assertEqual(meta.get("version"), "3.0.0")
        self.assertEqual(meta.get("type"), "EiffelArtifactReusedEvent")
        self.assertEqual(meta.get("id"), "0284875e-4f2f-4589-b6df-797afb039b88")
        self.assertEqual(meta.get("time"), 1575985114977)
