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
"""Base schemas and schema generation."""
import json
import os

import graphene
from graphene import relay

from ..db.database import get_database
from .lib.generic import BASE_JSON, convert


class EiffelConnectionField(relay.ConnectionField):
    """Base eiffel connection field."""

    def __init__(self, field):
        """Initialize schema fields."""
        field = "eiffel_graphql_api.graphql.schemas.events.{}".format(field)
        # pylint:disable=super-with-arguments
        super(EiffelConnectionField, self).__init__(field, search=graphene.String())


class BaseQuery(graphene.ObjectType):
    """Base query object type."""

    @classmethod
    def _clean_query(cls, query):
        """Format GraphQL query to MongoDB.

        Since queries in GraphQL are wrapped with double quotes (") and MongoDB also
        requires double quotes ("), we need to replace all single quotes (') with
        double quotes (")

        search: "{'search': 'value'}"
        = {'search': 'value'}
        Convert to: {"search": "value"}
        """
        return json.loads(query.replace("'", '"'))

    @classmethod
    def generic_resolve(
        cls, parent, info, last=None, first=None, search=None, **_
    ):  # pylint:disable=too-many-arguments, unused-argument
        """Generically resolve a meta node for each eiffel object type."""
        # pylint:disable=protected-access
        obj = info.return_type.graphene_type._meta.node
        collection = "Eiffel{}Event".format(obj)

        search = "{}" if search is None else search
        search = cls._clean_query(search)

        query = get_database()[collection].find(search)
        if last:
            query.limit(last)
            query.sort([("meta.time", -1)])
        elif first:
            query.limit(first)
            query.sort([("meta.time", 1)])
        else:
            query.sort([("meta.time", -1)])
        return [obj(mongo) for mongo in query]


# Generate the base query objecttype and it's resolve methods.
QUERY = {}
for ROOT, _, FILES in os.walk(BASE_JSON):
    for NAME in FILES:
        NAME = NAME.replace("Eiffel", "")
        NAME = NAME.replace("Event", "")
        NAME = NAME.replace(".json", "")
        CONNECTION_NAME = "{}Connection".format(NAME)
        RESOLVE_NAME = "resolve_{}".format(convert(NAME))
        SNAKE_NAME = convert(NAME)
        QUERY[SNAKE_NAME] = EiffelConnectionField(CONNECTION_NAME)
        QUERY[RESOLVE_NAME] = BaseQuery.generic_resolve

Query = type("Query", (BaseQuery,), QUERY)


SCHEMA = graphene.Schema(query=Query)
