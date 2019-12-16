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
from .activity_execution import ActivityExecution, PreviousActivityExecution
from .artifact import Artifact, ArtifactPreviousVersion, ReusedArtifact
from .cause import Cause
from .composition import Composition, CompositionPreviousVersion
from .confidence_level import SubConfidenceLevel
from .context import Context
from .element import Element
from .environment import Environment, EnvironmentPreviousVersion
from .flow_context import FlowContext
from .modified_announcement import ModifiedAnnouncement
from .subject import Subject
from .issues import *
from .iut import IUT
from .verification_basis import VerificationBasis
from .source_change_base import *
from .test_case_execution import *
from .test_suite_execution import *
from .tercc import Tercc


LINKS = {
    "CONTEXT": Context,
    "FLOW_CONTEXT": FlowContext,
    "CAUSE": Cause,
    "ACTIVITY_EXECUTION": ActivityExecution,
    "PREVIOUS_ACTIVITY_EXECUTION": PreviousActivityExecution,
    "MODIFIED_ANNOUNCEMENT": ModifiedAnnouncement,
    "COMPOSITION": Composition,
    "PREVIOUS_VERSION": {"EiffelArtifactCreatedEvent": ArtifactPreviousVersion,
                         "EiffelCompositionDefinedEvent": CompositionPreviousVersion,
                         "EiffelEnvironmentDefinedEvent": EnvironmentPreviousVersion,
                         "EiffelSourceChangeCreatedEvent": SourceCreatedPreviousVersion,
                         "EiffelSourceChangeSubmittedEvent": SourceSubmittedPreviousVersion},
    "ENVIRONMENT": Environment,
    "ARTIFACT": Artifact,
    "REUSED_ARTIFACT": ReusedArtifact,
    "ELEMENT": Element,
    "SUBJECT": Subject,
    "SUB_CONFIDENCE_LEVEL": SubConfidenceLevel,
    "SUCCESSFUL_ISSUE": SuccessfulIssue,
    "FAILED_ISSUE": FailedIssue,
    "INCONCLUSIVE_ISSUE": InconclusiveIssue,
    "IUT": IUT,
    "VERIFICATION_BASIS": VerificationBasis,
    "BASE": Base,
    "PARTIALLY_RESOLVE_ISSUE": PartiallyResolvedIssue,
    "RESOLVED_ISSUE": ResolvedIssue,
    "DERESOLVED_ISSUE": DeresolvedIssue,
    "CHANGE": SourceChange,
    "TEST_CASE_EXECUTION": TestCaseExecution,
    "TEST_SUITE_EXECUTION": TestSuiteExecution,
    "TERCC": Tercc,
}
