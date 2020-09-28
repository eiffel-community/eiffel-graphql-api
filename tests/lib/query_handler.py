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
"""Graphql query handler."""
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport


class GraphQLQueryHandler:
    """Create and send graphql queries."""

    __client = None
    __query = None

    def __init__(self, server):
        """Graphql query handler."""
        self.transport_protocol = RequestsHTTPTransport
        self.server = server

    @property
    def transport(self):
        """Transport protocol used for graphql."""
        return self.transport_protocol(self.server)

    @property
    def client(self):
        """Graphql client."""
        if self.__client is None:
            self.__client = Client(transport=self.transport)
        return self.__client

    @staticmethod
    def query(query):
        """Create a query for graphql.

        :param query: Query to make.
        :type query: str
        :return: Graphql formatted query.
        :rtype: :obj:`gql`
        """
        return gql(query)

    def execute(self, query):
        """Execute query against graphql.

        :param query: Query to make.
        :type query: str
        :return: Result from query.
        :rtype: dict
        """
        return self.client.execute(self.query(query))

    def search(self, dictionary, *keys):
        """Recursively search for keys in a nested dictionary.

        :param dictionary: Dictionary to search in.
        :type dictionary: dict
        :param keys: Keys to search for.
        :type keys: list
        :return: key and value matching the search.
        :rtype: tuple
        """
        for key, value in dictionary.items():
            if key in keys:
                yield key, value
            if isinstance(value, dict):
                for dict_key, dict_value in self.search(value, *keys):
                    yield dict_key, dict_value
            elif isinstance(value, (list, tuple)):
                for item in value:
                    if isinstance(item, dict):
                        for dict_key, dict_value in self.search(item, *keys):
                            yield dict_key, dict_value

    def get_node(self, response, node):
        """Get a node from response.

        :param response: GraphQL response dictionary.
        :type response: dict
        :param node: Node to get.
        :type node: dict
        :return: node dictionary.
        :rtype: dict
        """
        for _, response_node in self.search_for_nodes(response, node):
            return response_node

    def search_for_nodes(self, response, *nodes):
        """Search for nodes in a GraphQL response. Iterator.

        :param response: GraphQL response dictionary.
        :type response: dict
        :param nodes: Nodes to search for.
                      They are represented as keys in the response dict.
        :type nodes: list
        :return: Node name and node dictionary.
        :rtype: tuple
        """
        for node_name, edge in self.search(response, *nodes):
            if isinstance(edge, dict) and edge.get("edges") is not None:
                for node in edge.get("edges"):
                    yield node_name, node["node"]
            else:
                yield node_name, edge

    def search_for_node_typename(self, response, *nodes):
        """Search for nodes in a GraphQL response. Iterator.

        :param response: GraphQL response dictionary.
        :type response: dict
        :param nodes: Nodes to search for.
                      They are represented as keys in the response dict.
        :type list:
        :return: Node name and node dictionary.
        :rtype: tuple
        """
        for _, node in self.search(response, "node"):
            if node.get("__typename") in nodes:
                yield node.get("__typename"), node
