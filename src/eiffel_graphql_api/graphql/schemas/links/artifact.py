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
"""Eiffel Artifact links."""
import graphene

from eiffel_graphql_api.graphql.schemas.events import ArtifactCreated

from ..utils import find_one


class Artifact(graphene.ObjectType):
    """Artifact link."""

    artifact_created = graphene.Field(ArtifactCreated)

    def __init__(self, link):
        """Initialize link."""
        # pylint:disable=super-init-not-called
        self.link = link

    def resolve_artifact_created(self, _):
        """Resolve artifact created link."""
        from ..union import NotFound  # pylint:disable=import-outside-toplevel

        event = find_one(
            "EiffelArtifactCreatedEvent", {"meta.id": self.link.get("target")}
        )
        if event is None:
            return NotFound(self.link, "Could not find event in database.")
        return ArtifactCreated(event)


class ReusedArtifact(graphene.ObjectType):
    """Reused artifact link."""

    artifact_created = graphene.Field(ArtifactCreated)

    def __init__(self, link):
        """Initialize link."""
        # pylint:disable=super-init-not-called
        self.link = link

    def resolve_artifact_created(self, _):
        """Resolve artifact created link."""
        from ..union import NotFound  # pylint:disable=import-outside-toplevel

        event = find_one(
            "EiffelArtifactCreatedEvent", {"meta.id": self.link.get("target")}
        )
        if event is None:
            return NotFound(self.link, "Could not find event in database.")
        return ArtifactCreated(event)


class ArtifactPreviousVersion(graphene.ObjectType):
    """Previous artifact version link."""

    artifact_created = graphene.Field(ArtifactCreated)

    def __init__(self, link):
        """Initialize link."""
        # pylint:disable=super-init-not-called
        self.link = link

    def resolve_artifact_created(self, _):
        """Resolve artifact created link."""
        from ..union import NotFound  # pylint:disable=import-outside-toplevel

        event = find_one(
            "EiffelArtifactCreatedEvent", {"meta.id": self.link.get("target")}
        )
        if event is None:
            return NotFound(self.link, "Could not find event in database.")
        return ArtifactCreated(event)
