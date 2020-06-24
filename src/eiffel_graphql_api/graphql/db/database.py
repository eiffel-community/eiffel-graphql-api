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
"""Database handler functions."""
import os
import logging
import time
import math
import urllib.parse
from threading import Lock

import pymongo

DATABASE = None
CLIENT = None
LOCK = Lock()
LOGGER = logging.getLogger("Database")
RETRY_TIMEOUT = os.getenv("MONGODB_RECONNECT_TIMEOUT") or math.inf
# pylint: disable=global-statement


def connect(mock):
    """Connect and wait for connection to MongoDB.

    :param mock: Whether the server should be mocked or not. Used for tests.
    :type mock: bool
    """
    global DATABASE, CLIENT
    host = os.getenv("MONGODB_HOST", "localhost")
    port = os.getenv("MONGODB_PORT", "27017")
    username = os.getenv("MONGODB_USERNAME")
    password = os.getenv("MONGODB_PASSWORD")
    database_name = os.getenv("DATABASE_NAME", "this_is_not_correct")
    replicaset = os.getenv("MONGODB_REPLICASET") or None
    LOGGER.info("Connecting to %r:%r", host, port)

    if mock:
        # pylint: disable=import-outside-toplevel, import-error
        import mongomock
        mongo_client = mongomock.MongoClient
    else:
        mongo_client = pymongo.MongoClient

    if username and password:
        url = "mongodb://{}:{}@{}:{}".format(urllib.parse.quote(username),
                                             urllib.parse.quote(password),
                                             host, port)
    else:
        url = "mongodb://{}:{}".format(host, port)
    CLIENT = mongo_client(url, replicaset=replicaset)
    DATABASE = CLIENT[database_name]
    # 'server_info' will create a connection against the MongoDB effectively testing
    # the connection for us. This means that the 'connect' method will block until
    # a connection can be established or 'ServerSelectionTimeoutError' is raised.
    LOGGER.info("%r", CLIENT.server_info())
    LOGGER.info("Connected.")


def retry(fixture, timeout, *args, **kwargs):
    """Retry call to fixture for 'timeout' seconds.

    :param fixture: Fixture to call upon.
    :type fixture: :obj:`func`
    :param timeout: How long to wait for fixture to succeed. In seconds.
    :type timeout: float
    :param args: Positional argument to pass onto fixture.
    :type args: tuple
    :param kwargs: Keyword arguments to pass onto fixture.
    :type kwargs: dict
    """
    end = time.time() + timeout
    while time.time() < end:
        try:
            fixture(*args, **kwargs)
            break
        except Exception as exception:  # pylint:disable=broad-except
            LOGGER.warning("%r", exception)
            LOGGER.warning("Retrying %r", fixture)
            time.sleep(0.1)
    else:
        raise TimeoutError("Timeout after %rs calling fixture %r" % (timeout, fixture))


def get_database(mock=False):
    """Create and wait for a database connection.

    :param mock: Whether the server should be mocked or not. Used for tests.
    :type mock: bool
    :return: Database instance.
    :rtype: :obj:`pymongo.MongoClient.collection`
    """
    global DATABASE
    if DATABASE is None:
        retry(connect, float(RETRY_TIMEOUT), mock)
    return DATABASE


def get_client(mock=False):
    """Create and wait for a client connection.

    :param mock: Whether the server should be mocked or not. Used for tests.
    :type mock: bool
    :return: Client instance.
    :rtype: :obj:`pymongo.MongoClient`
    """
    global CLIENT
    if CLIENT is None:
        retry(connect, float(RETRY_TIMEOUT), mock)
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
    global DATABASE
    if DATABASE is None:
        with LOCK:
            DATABASE = get_database()
        return False  # Requeue event if DATABASE is not ready.
    try:
        collection = DATABASE[event.meta.type]
        collection.create_index([("meta.id", pymongo.ASCENDING)])
        collection.create_index([("links.target", pymongo.ASCENDING)])
        doc = event.json
        doc['_id'] = event.meta.event_id
        collection.insert_one(doc)
    except pymongo.errors.DuplicateKeyError:
        LOGGER.warning("Event already exists in the database, "
                       "skipping: %r", event.json)
        return True
    except Exception as exception:  # pylint:disable=broad-except
        LOGGER.warning("%r", exception)
        with LOCK:
            DATABASE = None
        return False
    return True
