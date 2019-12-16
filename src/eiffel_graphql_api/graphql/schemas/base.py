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
from datetime import datetime
import graphene
from graphene import relay
from .utils import find_type, search, multi_search
from .lib.generic import json_schema_to_graphql, load


class EiffelObjectType(graphene.ObjectType):
    links = graphene.List("eiffel_graphql_api.graphql.schemas.union.EiffelLinkUnion")
    reverse = relay.ConnectionField("eiffel_graphql_api.graphql.schemas.union.ReverseConnection")
    meta = json_schema_to_graphql(
        "EiffelMeta",
        load("EiffelActivityCanceledEvent.json").get("meta").get("properties"),
    )

    def search(self, filter, *args, **kwargs):
        return search(filter, *args, **kwargs)

    def find_type(self, type_name):
        return find_type(type_name)

    def resolve_links(self, info):
        from .links.utils import LINKS
        links = []
        print(self.mongo)
        for data in self.mongo.get("links", []):
            link = LINKS.get(data["type"])
            if isinstance(link, dict):
                links.append(link.get(self.mongo["meta"]["type"])(data))
            else:
                links.append(link(data))
        return links

    def resolve_meta(self, info):
        return info.return_type.graphene_type(self.mongo.get("meta"))

    def resolve_data(self, info):
        return info.return_type.graphene_type(self.mongo.get("data"))

    def resolve_reverse(self, info):
        events = []
        for event in multi_search({"links.target": self.mongo.get("meta", {}).get("id")}):
            obj = self.find_type(event["meta"]["type"])(event)
            events.append(obj)
        return events
