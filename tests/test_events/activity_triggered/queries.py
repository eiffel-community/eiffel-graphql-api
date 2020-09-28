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
"""Activity triggered queries."""

DATA_NAME_ONLY = """{
  activityTriggered {
    edges {
      node {
        data {
          name
        }
      }
    }
  }
}
"""

DATA_ONLY = """{
  activityTriggered {
    edges {
      node {
        data {
          name
          categories {
            type
          }
          activityTriggers {
            type
            description
          }
          executionType
        }
      }
    }
  }
}
"""

META_ONLY = """{
  activityTriggered {
    edges {
      node {
        meta {
          version
          id
          time
          type
        }
      }
    }
  }
}
"""

LINKS_ONLY = """{
  activityTriggered {
    edges {
      node {
        links {
          __typename
        }
      }
    }
  }
}
"""

CONTEXT_LINK = """{
  activityTriggered {
    edges {
      node {
        links {
          ... on Context {
            __typename
          }
        }
      }
    }
  }
}
"""

CONTEXT_LINK_TO_ACTIVITY_TRIGGERED = """{
  activityTriggered(search:"{'data.name': 'Activity triggered with activity context'}") {
    edges {
      node {
        links {
          ... on Context {
            link {
              ... on ActivityTriggered {
                meta {
                  id
                  type
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

CONTEXT_LINK_TO_TEST_SUITE_STARTED = """{
  activityTriggered(search:"{'data.name': 'Activity triggered with test suite context'}") {
    edges {
      node {
        links {
          ... on Context {
            link {
              ... on TestSuiteStarted {
                meta {
                  id
                  type
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

CAUSE_LINK = """{
  activityTriggered(search:"{'data.name': 'Activity triggered with cause link'}") {
    edges {
      node {
        links {
          ... on Cause {
            links {
              ... on ActivityTriggered {
                meta {
                  id
                  type
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

FLOW_CONTEXT_LINK = """{
  activityTriggered(search:"{'data.name': 'Activity triggered with flow context'}") {
    edges {
      node {
        links {
          ... on FlowContext {
            flowContextDefined {
              meta {
                id
                type
              }
            }
          }
        }
      }
    }
  }
}
"""
