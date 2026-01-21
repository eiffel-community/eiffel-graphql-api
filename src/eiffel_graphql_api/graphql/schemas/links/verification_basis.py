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
"""Eiffel verification basis link."""

import graphene

from ..utils import find_type, search


class VerificationBasis(graphene.ObjectType):
    """Verification basis link."""

    link = graphene.Field(
        "eiffel_graphql_api.graphql.schemas.union.EiffelVerificationBasisUnion"
    )

    def __init__(self, link):
        """Initialize link."""
        # pylint:disable=super-init-not-called
        self.link = link

    def resolve_link(self, _):
        """Resolve verification basis link."""
        from ..union import NotFound  # pylint:disable=import-outside-toplevel

        mongo = search({"meta.id": self.link.get("target")})
        if mongo is None:
            return NotFound(self.link, "Could not find event in database.")
        event = find_type(mongo["meta"]["type"])
        return event(mongo)
