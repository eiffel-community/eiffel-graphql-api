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
"""Eiffel GraphQL unions.

A union is an object type that can return one of several object types.
"""
# pylint: disable=wildcard-import, unused-wildcard-import
import graphene
from graphene import relay

from .events import *
from .links import *


class NotFound(graphene.ObjectType):
    """Link not found object type."""

    target = graphene.String()
    type = graphene.String()
    reason = graphene.String()
    mongo = None

    def __init__(self, link, reason):
        """Initialize link."""
        # pylint:disable=super-init-not-called
        self.mongo = {}
        self.link = link
        self.reason = reason

    def resolve_target(self, _):
        """Resolve link target."""
        return self.link.get("target")

    def resolve_type(self, _):
        """Resolve link type."""
        return self.link.get("type")

    def resolve_reason(self, _):
        """Resolve NotFound reason."""
        return self.reason


class EiffelContextUnion(graphene.Union):  # pylint: disable=too-few-public-methods
    """Eiffel context union."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Possible response object types."""

        types = (ActivityTriggered, TestSuiteStarted, NotFound)


class EiffelIutUnion(graphene.Union):  # pylint: disable=too-few-public-methods
    """Iut union."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Possible response object types."""

        types = (ArtifactCreated, CompositionDefined, NotFound)


class EiffelElementUnion(graphene.Union):  # pylint: disable=too-few-public-methods
    """Element union."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Possible response object types."""

        types = (CompositionDefined, ArtifactCreated, SourceChangeSubmitted, NotFound)


class EiffelVerificationBasisUnion(
    graphene.Union
):  # pylint: disable=too-few-public-methods
    """Verification basis union."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Possible response object types."""

        types = (TestCaseFinished, TestSuiteFinished, NotFound)


class EiffelSubjectUnion(graphene.Union):  # pylint: disable=too-few-public-methods
    """Subject union."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Possible response object types."""

        types = (
            CompositionDefined,
            ArtifactCreated,
            SourceChangeSubmitted,
            SourceChangeCreated,
            NotFound,
        )


class EiffelEventUnion(graphene.Union):  # pylint: disable=too-few-public-methods
    """Base event union."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Possible response object types."""

        types = (
            ActivityTriggered,
            ActivityStarted,
            ActivityFinished,
            ActivityCanceled,
            AnnouncementPublished,
            ArtifactCreated,
            ArtifactPublished,
            ArtifactReused,
            CompositionDefined,
            ConfidenceLevelModified,
            EnvironmentDefined,
            FlowContextDefined,
            IssueDefined,
            IssueVerified,
            SourceChangeCreated,
            SourceChangeSubmitted,
            TestCaseCanceled,
            TestCaseFinished,
            TestCaseStarted,
            TestCaseTriggered,
            TestExecutionRecipeCollectionCreated,
            TestSuiteFinished,
            TestSuiteStarted,
            NotFound,
        )


class EiffelLinkUnion(graphene.Union):  # pylint: disable=too-few-public-methods
    """Base link union."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Possible response object types."""

        types = (
            Context,
            FlowContext,
            Cause,
            ActivityExecution,
            PreviousActivityExecution,
            ModifiedAnnouncement,
            Composition,
            CompositionPreviousVersion,
            Environment,
            ArtifactPreviousVersion,
            Artifact,
            ReusedArtifact,
            Element,
            Subject,
            SubConfidenceLevel,
            EnvironmentPreviousVersion,
            SuccessfulIssue,
            FailedIssue,
            InconclusiveIssue,
            IUT,
            Base,
            SourceCreatedPreviousVersion,
            PartiallyResolvedIssue,
            ResolvedIssue,
            DeresolvedIssue,
            SourceChange,
            SourceSubmittedPreviousVersion,
            TestCaseExecution,
            TestSuiteExecution,
            Tercc,
        )


class ReverseConnection(relay.Connection):  # pylint: disable=too-few-public-methods
    """Reverse search connection."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Possible response object types."""

        node = EiffelEventUnion
