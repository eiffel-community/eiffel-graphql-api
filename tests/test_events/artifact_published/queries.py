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
"""Artifact published queries."""

DATA_ONLY = """{
  artifactPublished {
    edges {
      node {
        data {
          locations {
            type
            uri
          }
        }
      }
    }
  }
}
"""

META_ONLY = """{
  artifactPublished {
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
  artifactPublished {
    edges {
      node {
        links {
          ... on Artifact {
            artifactCreated {
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
