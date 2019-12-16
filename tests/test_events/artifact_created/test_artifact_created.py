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


class TestArtifactCreated(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.query_handler = GraphQLQueryHandler("http://127.0.0.1:12345/graphql")
        cls.events = [
            eiffel_artifact_created_event()
        ]
        cls.logger = logging.getLogger("TestArtifactCreated")

    def setUp(self):
        self.logger.info("\n")
        for event in self.events:
            insert(event)

    def tearDown(self):
        for event in self.events:
            remove(event)

    def test_artifact_created_data(self):
        """Test that it is possible to query 'data' from artifact created.

        Approval criteria:
            - It shall be possible to query 'data' from graphql.
            - Data shall be:
                - identity: "pkg:artifact/created/test@1.0.0"
                - fileInformation: {"name": "a_file.txt", "tags": ["EPIC_TEST_FILE"]}
                - buildCommand: "pytest"
                - implements: ["pkg:composition/link/test@1.0.0"]
                - dependsOn: ["pkg:environment/link/test@1.0.0"]
                - name: "TestingArtifact"

        Test steps:
            1. Query 'data' from ArtifactCreated in Graphql.
            2. Verify that the response is correct.
        """
        self.logger.info("STEP: Query 'data' from ArtifactCreated in Graphql.")
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
                "identity": "pkg:artifact/created/test@1.0.0",
                "fileInformation": [
                    {
                        "name": "a_file.txt",
                        "artifactTags": [
                            {"type": "EPIC_TEST_FILE"}
                        ]
                    }
                ],
                "buildCommand": "pytest",
                "requiresImplementation": "ANY",
                "implements": [
                    {"type": "pkg:composition/link/test@1.0.0"}
                ],
                "dependsOn": [
                    {"type": "pkg:environment/link/test@1.0.0"}
                ],
                "name": "TestingArtifact"
            }
        )

    def test_artifact_created_composition_link(self):
        """Test that it is possible to query a valid composition link on artifact created.

        Approval criteria:
            - Graphql shall return an CompositionDefined event when requesting Composition.

        Test steps:
            1. Query 'links.Composition' from ArtifactCreated in Graphql.
            2. Verify that the returned event is a CompositionDefined.
        """
        events =[
            eiffel_composition_defined(),
            eiffel_artifact_created_event_composition_link()
        ]
        try:
            for event in events:
                insert(event)
            self.logger.info("STEP: Query 'links.Composition' from ArtifactCreated in Graphql.")
            self.logger.debug(LINKS_COMPOSITION_DEFINED)
            response = self.query_handler.execute(LINKS_COMPOSITION_DEFINED)
            self.logger.debug(pretty(response))

            self.logger.info("STEP: Verify that the returned event is a CompositionDefined.")
            link_meta = self.query_handler.get_node(response, "meta")
            self.assertDictEqual(link_meta, {"id": "460ff165-125d-468f-a5d2-677d5a939507",
                                             "type": "EiffelCompositionDefinedEvent"})
        finally:
            for event in events:
                remove(event)

    def test_artifact_created_environment_link(self):
        """Test that it is possible to query a valid environment link on artifact created.

        Approval criteria:
            - Graphql shall return an EnvironmentDefined event when requesting Environment.

        Test steps:
            1. Query 'links.Environment' from ArtifactCreated in Graphql.
            2. Verify that the returned event is an EnvironmentDefined.
        """
        events =[
            eiffel_environment_defined(),
            eiffel_artifact_created_event_environment_link()
        ]
        try:
            for event in events:
                insert(event)
            self.logger.info("STEP: Query 'links.Environment' from ArtifactCreated in Graphql.")
            self.logger.debug(LINKS_ENVIRONMENT_DEFINED)
            response = self.query_handler.execute(LINKS_ENVIRONMENT_DEFINED)
            self.logger.debug(pretty(response))

            self.logger.info("STEP: Verify that the returned event is an EnvironmentDefined.")
            link_meta = self.query_handler.get_node(response, "meta")
            self.assertDictEqual(link_meta, {"id": "0639dc49-8f4f-4732-899e-3aefc66a5bfb",
                                             "type": "EiffelEnvironmentDefinedEvent"})
        finally:
            for event in events:
                remove(event)

    def test_artifact_created_previous_link(self):
        """Test that it is possible to query a valid previous link on artifact created.

        Approval criteria:
            - Graphql shall return an ArtifactCreated event when requesting ArtifactPreviousVersion.

        Test steps:
            1. Query 'links.ArtifactPreviousVersion' from ArtifactCreated in Graphql.
            2. Verify that the returned event is an ArtifactCreated.
        """
        event = eiffel_artifact_created_event_previous_version_link()
        try:
            insert(event)
            self.logger.info("STEP: Query 'links.ArtifactPreviousVersion' from ArtifactCreated in Graphql.")
            self.logger.debug(LINKS_PREVIOUS_VERSION)
            response = self.query_handler.execute(LINKS_PREVIOUS_VERSION)
            self.logger.debug(pretty(response))

            self.logger.info("STEP: Verify that the returned event is an EnvironmentDefined.")
            link_meta = self.query_handler.get_node(response, "meta")
            self.assertDictEqual(link_meta, {"id": "730f8573-cd69-41f5-81ad-d85aebf28d03",
                                             "type": "EiffelArtifactCreatedEvent"})
        finally:
            remove(event)

    def test_artifact_created_meta(self):
        """Test that it is possible to query 'meta' from artifact created.

        Approval criteria:
            - It shall be possible to query 'meta' from graphql.
            - Data returned shall be correct:
                - version: "3.0.0"
                - type   : "EiffelArtifactCreatedEvent"
                - id     : "730f8573-cd69-41f5-81ad-d85aebf28d03"
                - time   : 1575968228603

        Test steps:
            1. Query 'meta' from  ArtifactCreated in Graphql.
            2. Verify that the response is not empty.
            3. Verify that meta data returned correctly.
        """
        self.logger.info("STEP: Query 'meta' from ArtifactCreated in Graphql.")
        self.logger.debug(META_ONLY)
        response = self.query_handler.execute(META_ONLY)
        self.logger.debug(pretty(response))

        self.logger.info("STEP: Verify that response is not empty.")
        meta = self.query_handler.get_node(response, "meta")
        self.assertIsInstance(meta, dict)
        self.assertGreater(len(meta), 0)

        self.logger.info("STEP: Verify that meta data returned correctly.")
        self.assertEqual(meta.get("version"), "3.0.0")
        self.assertEqual(meta.get("type"), "EiffelArtifactCreatedEvent")
        self.assertEqual(meta.get("id"), "730f8573-cd69-41f5-81ad-d85aebf28d03")
        self.assertEqual(meta.get("time"), "2019-12-10T09:57:08.603000")
