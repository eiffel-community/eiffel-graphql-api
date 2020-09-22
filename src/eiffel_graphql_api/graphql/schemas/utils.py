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
"""Utility functions."""
from ..db.database import get_database


def search(filter, *args, **kwargs):  # pylint:disable=redefined-builtin
    """Search for filter in MongoDB.

    :param filter: Filter to search for.
    :type filter: dict
    :return: Response from MongoDB search.
    :rtype: dict
    """
    database = get_database()
    for collection in database.list_collection_names():
        response = database[collection].find_one(filter, *args, **kwargs)
        if response:
            return response
    return None


def multi_search(filter, *args, **kwargs):  # pylint:disable=redefined-builtin
    """Search for multiple items in MongoDB.

    :param filter: Filter to search for.
    :type filter: dict
    :return: Response from MongoDB search.
    :rtype: dict
    """
    database = get_database()
    responses = []
    for collection in database.list_collection_names():
        response = database[collection].find(filter, *args, **kwargs)
        responses += list(response)
    return responses


def find_one(collection, filter, *args, **kwargs):  # pylint:disable=redefined-builtin
    """Find a single item from MongoDB collection.

    :param collection: From which collection to get item.
    :type collection: str
    :param filter: Filter to search for.
    :type filter: dict
    :return: Response from MongoDB search.
    :rtype: dict
    """
    database = get_database()
    return database[collection].find_one(filter, *args, **kwargs)


def find_type(type_name):
    """Find Eiffel object type from name.

    :param type_name: Name of object type to find.
    :type type_name: str
    :return: GraphQL schema object type.
    :rtype: :obj:`graphene.ObjectType`
    """
    # pylint: disable=import-outside-toplevel
    from eiffel_graphql_api.graphql.schemas.events import EVENTS

    return EVENTS.get(type_name)
