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
"""Base object type."""
import graphene
from graphene import relay

from .lib.generic import json_schema_to_graphql, load
from .utils import find_type, multi_search, search


class EiffelObjectType(graphene.ObjectType):
    """Eiffel event base object type."""

    links = graphene.List("eiffel_graphql_api.graphql.schemas.union.EiffelLinkUnion")
    reverse = relay.ConnectionField(
        "eiffel_graphql_api.graphql.schemas.union.ReverseConnection"
    )
    meta = json_schema_to_graphql(
        "EiffelMeta",
        load("EiffelActivityCanceledEvent.json").get("meta").get("properties"),
    )
    mongo = None

    @staticmethod
    def search(filter, *args, **kwargs):  # pylint:disable=redefined-builtin
        """Search for event in DB.

        :param filter: MongoDB filter.
        :type filter: dict
        :return: JSON result from database search.
        :rtype: dict
        """
        return search(filter, *args, **kwargs)

    @staticmethod
    def find_type(type_name):
        """Find Eiffel object type from type name.

        :param type_name: Name of type to find.
        :type type_name: str
        :return: GraphQL schema for event type.
        :rtype: :obj:`graphene.ObjectType`
        """
        return find_type(type_name)

    def resolve_links(self, _):
        """Resolve eiffel links on 'links' GraphQL query."""
        # pylint:disable=import-outside-toplevel
        # pylint:disable=unsubscriptable-object
        from .links.utils import LINKS

        links = []
        for data in self.mongo.get("links", []):
            link = LINKS.get(data["type"])
            if isinstance(link, dict):
                links.append(link.get(self.mongo["meta"]["type"])(data))
            else:
                links.append(link(data))
        return links

    def resolve_meta(self, info):
        """Resolve eiffel meta on 'meta' GraphQL query."""
        return info.return_type.graphene_type(self.mongo.get("meta"))

    def resolve_data(self, info):
        """Resolve eiffel data on 'data' GraphQL query."""
        return info.return_type.graphene_type(self.mongo.get("data"))

    def resolve_reverse(self, _):
        """Resolve reverse searching for link references."""
        events = []
        for event in multi_search(
            {"links.target": self.mongo.get("meta", {}).get("id")}
        ):
            obj = self.find_type(event["meta"]["type"])(event)
            events.append(obj)
        return events
