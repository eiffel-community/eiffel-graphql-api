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

DATA_ONLY = '''{
  artifactCreated {
    edges {
      node {
        data {
          identity
          fileInformation {
            name
            artifactTags {
              type
            }
          }
          buildCommand
          requiresImplementation
          implements {
            type
          }
          dependsOn {
            type
          }
          name
        }
      }
    }
  }
}
'''

META_ONLY = '''{
  artifactCreated {
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
'''


LINKS_COMPOSITION_DEFINED = '''{
  artifactCreated(search: "{'data.identity': 'pkg:composition/link/test@1.0.0'}") {
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
'''


LINKS_ENVIRONMENT_DEFINED = '''{
  artifactCreated(search: "{'data.identity': 'pkg:environment/link/test@1.0.0'}") {
    edges {
      node {
        links {
          ... on Environment {
            environmentDefined {
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
'''

LINKS_PREVIOUS_VERSION = '''{
  artifactCreated(search: "{'data.identity': 'pkg:previous_version/link/test@1.0.0'}") {
    edges {
      node {
        links {
          ... on ArtifactPreviousVersion {
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
'''
