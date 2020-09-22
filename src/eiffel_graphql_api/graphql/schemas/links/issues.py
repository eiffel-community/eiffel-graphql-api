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
"""Eiffel issues links."""
import graphene

from eiffel_graphql_api.graphql.schemas.events import IssueDefined

from ..utils import find_one


class SuccessfulIssue(graphene.ObjectType):
    """Successful issue link."""

    issue_defined = graphene.Field(IssueDefined)

    def __init__(self, link):
        """Initialize link."""
        # pylint:disable=super-init-not-called
        self.link = link

    def resolve_issue_defined(self, _):
        """Resolve issue defined link."""
        from ..union import NotFound  # pylint:disable=import-outside-toplevel

        event = find_one(
            "EiffelIssueDefinedEvent", {"meta.id": self.link.get("target")}
        )
        if event is None:
            return NotFound(self.link, "Could not find event in database.")
        return IssueDefined(event)


class FailedIssue(SuccessfulIssue):
    """Failed issue link."""


class InconclusiveIssue(SuccessfulIssue):
    """Inconclusive issue link."""


class PartiallyResolvedIssue(SuccessfulIssue):
    """Partially resolved issue link."""


class ResolvedIssue(SuccessfulIssue):
    """Resolved issue link."""


class DeresolvedIssue(SuccessfulIssue):
    """Deresolved issue link."""
