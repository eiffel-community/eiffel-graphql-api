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
"""Event helpers."""
import os
import json
from eiffel_graphql_api.graphql.db.database import get_database, get_client


def pretty(event):
    """Prettify an event for printing.

    :param event: Dictionary of Eiffel event.
    :type event: dict
    :return: Preffy json string.
    :rtype: str
    """
    return json.dumps(event, indent=4, sort_keys=True)


def insert(event):
    """Insert an event to the MongoDB database.

    :param event: Event to insert.
    :type event: dict
    """
    database = get_database(mock=True)
    if isinstance(event, list):
        for event_data in event:
            database[event_data["meta"]["type"]].insert_one(event_data)
    else:
        database[event["meta"]["type"]].insert_one(event)


def remove(event):
    """Remove an event from the MongoDB database.

    :param event: Event to remove.
    :type event: dict
    """
    database = get_database(mock=True)
    if isinstance(event, list):
        for event_data in event:
            database[event_data["meta"]["type"]].delete_one(event_data)
    else:
        database[event["meta"]["type"]].delete_one(event)


def drop():
    """Drop the MongoDB database."""
    get_client(mock=True).drop_database(os.getenv("MONGO_DB"))
