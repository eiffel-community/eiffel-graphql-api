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
import graphene
from graphene import relay
from .links import *

from .events import *


class NotFound(graphene.ObjectType):
    target = graphene.String()
    type = graphene.String()
    reason = graphene.String()
    mongo = None

    def __init__(self, link, reason):
        self.mongo = {}
        self.link = link
        self.reason = reason

    def resolve_target(self, info):
        return self.link.get("target")

    def resolve_type(self, info):
        return self.link.get("type")

    def resolve_reason(self, info):
        return self.reason


class EiffelContextUnion(graphene.Union):
    class Meta:
        types = (ActivityTriggered, TestSuiteStarted, NotFound)


class EiffelIutUnion(graphene.Union):
    class Meta:
        types = (ArtifactCreated, CompositionDefined, NotFound)


class EiffelElementUnion(graphene.Union):
    class Meta:
        types = (CompositionDefined, ArtifactCreated, SourceChangeSubmitted, NotFound)


class EiffelVerificationBasisUnion(graphene.Union):
    class Meta:
        types = (TestCaseFinished, TestSuiteFinished, NotFound)


class EiffelSubjectUnion(graphene.Union):
    class Meta:
        types = (CompositionDefined, ArtifactCreated, SourceChangeSubmitted,
                 SourceChangeCreated, NotFound)


class EiffelEventUnion(graphene.Union):
    class Meta:
        types = (ActivityTriggered, ActivityStarted, ActivityFinished, ActivityCanceled,
                 AnnouncementPublished, ArtifactCreated, ArtifactPublished, ArtifactReused,
                 CompositionDefined, ConfidenceLevelModified, EnvironmentDefined, FlowContextDefined,
                 IssueDefined, IssueVerified, SourceChangeCreated, SourceChangeSubmitted,
                 TestCaseCanceled, TestCaseFinished, TestCaseStarted, TestCaseTriggered,
                 TestExecutionRecipeCollectionCreated, TestSuiteFinished, TestSuiteStarted,
                 NotFound)


class EiffelLinkUnion(graphene.Union):
    class Meta:
        types = (Context, FlowContext, Cause,
                 ActivityExecution, PreviousActivityExecution,
                 ModifiedAnnouncement, Composition, CompositionPreviousVersion,
                 Environment, ArtifactPreviousVersion, Artifact,
                 ReusedArtifact, Element, Subject, SubConfidenceLevel,
                 EnvironmentPreviousVersion, SuccessfulIssue, FailedIssue,
                 InconclusiveIssue, IUT, Base, SourceCreatedPreviousVersion,
                 PartiallyResolvedIssue, ResolvedIssue, DeresolvedIssue,
                 SourceChange, SourceSubmittedPreviousVersion, TestCaseExecution,
                 TestSuiteExecution, Tercc)


class ReverseConnection(relay.Connection):
    class Meta:
        node = EiffelEventUnion
