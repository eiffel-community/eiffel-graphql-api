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
"""Eiffel event objects and connecting Eiffel event names with objects."""

from .activity_canceled import ActivityCanceled, ActivityCanceledConnection
from .activity_finished import ActivityFinished, ActivityFinishedConnection
from .activity_started import ActivityStarted, ActivityStartedConnection
from .activity_triggered import ActivityTriggered, ActivityTriggeredConnection
from .announcement_published import (
    AnnouncementPublished,
    AnnouncementPublishedConnection,
)
from .artifact_created import ArtifactCreated, ArtifactCreatedConnection
from .artifact_published import ArtifactPublished, ArtifactPublishedConnection
from .artifact_reused import ArtifactReused, ArtifactReusedConnection
from .composition_defined import CompositionDefined, CompositionDefinedConnection
from .confidence_level_modified import (
    ConfidenceLevelModified,
    ConfidenceLevelModifiedConnection,
)
from .environment_defined import EnvironmentDefined, EnvironmentDefinedConnection
from .flow_context_defined import FlowContextDefined, FlowContextDefinedConnection
from .issue_defined import IssueDefined, IssueDefinedConnection
from .issue_verified import IssueVerified, IssueVerifiedConnection
from .source_change_created import SourceChangeCreated, SourceChangeCreatedConnection
from .source_change_submitted import (
    SourceChangeSubmitted,
    SourceChangeSubmittedConnection,
)
from .test_case_canceled import TestCaseCanceled, TestCaseCanceledConnection
from .test_case_finished import TestCaseFinished, TestCaseFinishedConnection
from .test_case_started import TestCaseStarted, TestCaseStartedConnection
from .test_case_triggered import TestCaseTriggered, TestCaseTriggeredConnection
from .test_execution_recipe_collection_created import (
    TestExecutionRecipeCollectionCreated,
    TestExecutionRecipeCollectionCreatedConnection,
)
from .test_suite_finished import TestSuiteFinished, TestSuiteFinishedConnection
from .test_suite_started import TestSuiteStarted, TestSuiteStartedConnection

EVENTS = {
    "EiffelActivityCanceledEvent": ActivityCanceled,
    "EiffelActivityFinishedEvent": ActivityFinished,
    "EiffelActivityStartedEvent": ActivityStarted,
    "EiffelActivityTriggeredEvent": ActivityTriggered,
    "EiffelAnnouncementPublishedEvent": AnnouncementPublished,
    "EiffelArtifactCreatedEvent": ArtifactCreated,
    "EiffelArtifactPublishedEvent": ArtifactPublished,
    "EiffelArtifactReusedEvent": ArtifactReused,
    "EiffelCompositionDefinedEvent": CompositionDefined,
    "EiffelConfidenceLevelModifiedEvent": ConfidenceLevelModified,
    "EiffelEnvironmentDefinedEvent": EnvironmentDefined,
    "EiffelFlowContextDefinedEVent": FlowContextDefined,
    "EiffelIssueDefinedEvent": IssueDefined,
    "EiffelIssueVerifiedEvent": IssueVerified,
    "EiffelSourceChangeCreatedEvent": SourceChangeCreated,
    "EiffelSourceChangeSubmittedEvent": SourceChangeSubmitted,
    "EiffelTestCaseCanceledEvent": TestCaseCanceled,
    "EiffelTestCaseFinishedEvent": TestCaseFinished,
    "EiffelTestCaseStartedEvent": TestCaseStarted,
    "EiffelTestCaseTriggeredEvent": TestCaseTriggered,
    "EiffelTestExecutionRecipeCollectionCreatedEvent": TestExecutionRecipeCollectionCreated,
    "EiffelTestSuiteFinishedEvent": TestSuiteFinished,
    "EiffelTestSuiteStartedEvent": TestSuiteStarted,
}
