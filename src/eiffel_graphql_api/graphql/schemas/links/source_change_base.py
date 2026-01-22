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
"""Eiffel source change links."""

import graphene

from eiffel_graphql_api.graphql.schemas.events import (
    SourceChangeCreated,
    SourceChangeSubmitted,
)

from ..utils import find_one


class Base(graphene.ObjectType):
    """Base link."""

    source_change_submitted = graphene.Field(SourceChangeSubmitted)

    def __init__(self, link):
        """Initialize link."""
        # pylint:disable=super-init-not-called
        self.link = link

    def resolve_source_change_submitted(self, _):
        """Resolve source change submitted link."""
        from ..union import NotFound  # pylint:disable=import-outside-toplevel

        event = find_one(
            "EiffelSourceChangeSubmittedEvent", {"meta.id": self.link.get("target")}
        )
        if event is None:
            return NotFound(self.link, "Could not find event in database.")
        return SourceChangeSubmitted(event)


class SourceChange(graphene.ObjectType):
    """Source change link."""

    source_change_created = graphene.Field(SourceChangeCreated)

    def __init__(self, link):
        """Initialize link."""
        # pylint:disable=super-init-not-called
        self.link = link

    def resolve_source_change_created(self, _):
        """Resolve source change created link."""
        from ..union import NotFound  # pylint:disable=import-outside-toplevel

        event = find_one(
            "EiffelSourceChangeCreatedEvent", {"meta.id": self.link.get("target")}
        )
        if event is None:
            return NotFound(self.link, "Could not find event in database.")
        return SourceChangeCreated(event)


class SourceSubmittedPreviousVersion(graphene.ObjectType):
    """Previous source submitted link."""

    source_change_submitted = graphene.Field(SourceChangeSubmitted)

    def __init__(self, link):
        """Initialize link."""
        # pylint:disable=super-init-not-called
        self.link = link

    def resolve_source_change_submitted(self, _):
        """Resolve source change submitted link."""
        from ..union import NotFound  # pylint:disable=import-outside-toplevel

        event = find_one(
            "EiffelSourceChangeSubmittedEvent", {"meta.id": self.link.get("target")}
        )
        if event is None:
            return NotFound(self.link, "Could not find event in database.")
        return SourceChangeSubmitted(event)


class SourceCreatedPreviousVersion(graphene.ObjectType):
    """Previous source created link."""

    source_change_created = graphene.Field(SourceChangeCreated)

    def __init__(self, link):
        """Initialize link."""
        # pylint:disable=super-init-not-called
        self.link = link

    def resolve_source_change_created(self, _):
        """Resolve source change created link."""
        from ..union import NotFound  # pylint:disable=import-outside-toplevel

        event = find_one(
            "EiffelSourceChangeCreatedEvent", {"meta.id": self.link.get("target")}
        )
        if event is None:
            return NotFound(self.link, "Could not find event in database.")
        return SourceChangeCreated(event)
