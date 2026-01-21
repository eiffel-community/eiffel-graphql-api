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
"""Resolve terc link."""

import graphene

from eiffel_graphql_api.graphql.schemas.events import (
    TestExecutionRecipeCollectionCreated,
)

from ..utils import find_one


class Terc(graphene.ObjectType):
    """Terc link."""

    test_execution_recipe_collection_created = graphene.Field(
        TestExecutionRecipeCollectionCreated
    )

    def __init__(self, link):
        """Initialize link."""
        # pylint:disable=super-init-not-called
        self.link = link

    def resolve_test_execution_recipe_collection_created(self, _):
        """Resolve terc link."""
        from ..union import NotFound  # pylint:disable=import-outside-toplevel

        event = find_one(
            "EiffelTestExecutionRecipeCollectionCreatedEvent",
            {"meta.id": self.link.get("target")},
        )
        if event is None:
            return NotFound(self.link, "Could not find event in database.")
        return TestExecutionRecipeCollectionCreated(event)
