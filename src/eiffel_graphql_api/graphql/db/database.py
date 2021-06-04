# Copyright 2019-2020 Axis Communications AB.
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
"""Database handler functions."""
import logging
import math
import os
import urllib.parse
from threading import Lock

import pymongo

DATABASE = None
CLIENT = None
LOCK = Lock()
LOGGER = logging.getLogger(__name__)
RETRY_TIMEOUT = os.getenv("MONGODB_RECONNECT_TIMEOUT") or math.inf
# pylint: disable=global-statement


class ConfigurationError(Exception):
    """Indicates a problem with a configuration setting."""


def connect(mock):
    """Connect and wait for connection to MongoDB.

    :param mock: Whether the server should be mocked or not. Used for tests.
    :type mock: bool
    """
    global DATABASE, CLIENT
    url = os.getenv("MONGODB_CONNSTRING")
    if not url:
        raise ConfigurationError(
            "The required MONGODB_CONNSTRING environment variable was "
            "unset or empty."
        )
    database_name = os.getenv("MONGODB_DATABASE")
    if not database_name:
        raise ConfigurationError(
            "The required MONGODB_DATABASE environment variable was unset or empty."
        )
    safe_url = url
    urlparts = urllib.parse.urlparse(url)
    if urlparts.password:
        safe_url = safe_url.replace(urlparts.password, "*****")
    LOGGER.info("Connecting to %s", safe_url)

    if mock:
        # pylint: disable=import-outside-toplevel, import-error
        import mongomock

        mongo_client = mongomock.MongoClient
    else:
        mongo_client = pymongo.MongoClient

    with LOCK:
        CLIENT = mongo_client(url)
        DATABASE = CLIENT[database_name]
    # 'server_info' will create a connection against the MongoDB effectively testing
    # the connection for us. This means that the 'connect' method will block until
    # a connection can be established or 'ServerSelectionTimeoutError' is raised.
    LOGGER.info("%r", CLIENT.server_info())
    LOGGER.info("Connected.")


def get_database(mock=False):
    """Create and wait for a database connection.

    :param mock: Whether the server should be mocked or not. Used for tests.
    :type mock: bool
    :return: Database instance.
    :rtype: :obj:`pymongo.database.Database`
    """
    if DATABASE is None:
        connect(mock)
    return DATABASE


def get_client(mock=False):
    """Create and wait for a client connection.

    :param mock: Whether the server should be mocked or not. Used for tests.
    :type mock: bool
    :return: Client instance.
    :rtype: :obj:`pymongo.MongoClient`
    """
    if CLIENT is None:
        connect(mock)
    return CLIENT


def insert_to_db(event, _=None):
    """Eiffel callback for storing events in database.

    :param event: Event to store into database.
    :type event: :obj:`eiffellib.events.eiffel_base_event.EiffelBaseEvent`
    :param context: In which context was the event sent.
    :type context: str
    :return: Whether or not database insertion succeeded.
    :rtype: bool
    """
    try:
        database = get_database()
        collection = database[event.meta.type]
        doc = event.json
        doc["_id"] = event.meta.event_id
        collection.insert_one(doc)
    except pymongo.errors.DuplicateKeyError:
        LOGGER.warning("Event already exists in the database, skipping: %r", event.json)
        return True
    except pymongo.errors.ConnectionFailure as exception:
        LOGGER.warning("%r", exception)
        return False
    return True
