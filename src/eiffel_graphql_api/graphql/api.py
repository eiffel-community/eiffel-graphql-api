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
"""Eiffel GraphQL Flask API APP."""

from flask import Flask
from graphql_server.flask.graphqlview import GraphQLView

from .schemas.schema import SCHEMA

APP = Flask(__name__)

APP.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=SCHEMA, graphiql=True)
)
