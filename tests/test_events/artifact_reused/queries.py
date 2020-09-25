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
"""Test artifact reused queries."""


META_ONLY = """{
  artifactReused {
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


LINKS_COMPOSITION = """{
  artifactReused(search: "{'meta.id': '0e5d23cc-e3ed-45e5-9370-9fbcfd260812'}") {
    edges {
      node {
        links {
          ... on Composition {
            compositionDefined {
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


LINKS_ARTIFACT = """{
  artifactReused(search: "{'meta.id': '88feb145-707c-49df-afdf-c0b80aca9cc3'}") {
    edges {
      node {
        links {
          ... on ReusedArtifact {
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
