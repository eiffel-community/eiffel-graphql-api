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
import os
import json
import graphene
from graphene import relay
from ..db.database import get_database
from .lib.generic import BASE_JSON, convert


class EiffelConnectionField(relay.ConnectionField):
    def __init__(self, field):
        field = "eiffel_graphql_api.graphql.schemas.events.{}".format(field)
        super(EiffelConnectionField, self).__init__(
            field,
            search=graphene.String()
        )


class BaseQuery(graphene.ObjectType):

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
    def generic_resolve(cls, parent, info, last=None, first=None, search=None, **_):
        """Generically resolve a meta node for each eiffel object type."""
        obj = info.return_type.graphene_type._meta.node
        collection = "Eiffel{}Event".format(obj)

        search = "{}" if search is None else search
        search = cls._clean_query(search)

        query = get_database()[collection].find(search)
        if last:
            query.limit(last)
            query.sort([("_id", -1)])
        elif first:
            query.limit(first)
            query.sort([("_id", 1)])
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
