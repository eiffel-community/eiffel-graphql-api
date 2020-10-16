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
"""Pytest configuration."""
import os
import threading
import time
import logging
import pytest
from requests.exceptions import HTTPError
from tests.lib.query_handler import GraphQLQueryHandler
from eiffel_graphql_api.graphql.api import APP
from eiffel_graphql_api.graphql.db.database import get_database
from eiffel_graphql_api.graphql.db.database import get_client


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


@pytest.fixture
def mock_mongo():
    """Inject a MongoDB client connected to a mock server.

    No database in place, guaranteeing that we'll start from a clean slate.
    """
    client = get_client(mock=True)
    client.drop_database(os.getenv("MONGODB_DATABASE"))
    yield get_database(mock=True)


def start():
    """Start a GraphQL API for testing."""
    APP.run("127.0.0.1", 12345)


def wait_for_webserver_connection():
    """Wait for the webserver to respond to HTTP requests."""
    LOGGER.info("Testing for webserver connectivity.")
    query_handler = GraphQLQueryHandler("http://127.0.0.1:12345/graphql")
    timeout = time.time() + 30
    while time.time() < timeout:
        try:
            query_handler.execute("{nothing}")
            LOGGER.info("Up and running")
            return
        except HTTPError:  # BadRequest means the webserver came up.
            LOGGER.info("Up and running")
            return
        except Exception as exception:  # pylint: disable=broad-except
            LOGGER.error("%r", exception)
        LOGGER.warning("Connection could not be established. Trying again in 1s..")
        time.sleep(1)
    raise TimeoutError("Timeout waiting for the webserver to start.")


@pytest.fixture(scope="session", autouse=True)
def start_server(
    request,
):  # Input must exist due to 'fixture'. pylint:disable=unused-argument
    """Start the Graphql API server in a thread. This is done once per test session."""
    client = get_client(mock=True)
    thread = threading.Thread(target=start)
    thread.daemon = True
    thread.start()
    wait_for_webserver_connection()
    client.drop_database(os.getenv("MONGODB_DATABASE"))

    def start_server_fin():  # pylint:disable=unused-variable
        """Drop the MongoDB database as a cleanup measure."""
        client.drop_database(os.getenv("MONGODB_DATABASE"))
