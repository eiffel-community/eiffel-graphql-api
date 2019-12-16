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
FOLLOW_MY_COMMIT = '''{
  sourceChangeCreated(search: "{'data.gitIdentifier.commitId': 'c9ea15d2d0d3bcfa2856416be4add5a5919764f4'}") {
    edges {
      node {
        reverse {
          edges {
            node {
              ... on SourceChangeSubmitted {
                reverse {
                  edges {
                    node {
                      ... on CompositionDefined {
                        reverse {
                          edges {
                            node {
                              ... on ArtifactCreated {
                                reverse {
                                  edges {
                                    node {
                                      __typename
                                      ... on ArtifactPublished {
                                        data {
                                          locations {
                                            uri
                                            type
                                          }
                                        }
                                      }
                                      ... on ConfidenceLevelModified {
                                        data {
                                          name
                                          value
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
'''
