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
import os
import pymongo

DATABASE = None
CLIENT = None


def connect(mock):
    global DATABASE, CLIENT
    host = os.getenv("MONGODB_HOST", "localhost")
    port = os.getenv("MONGODB_PORT", "27017")
    database_name = os.getenv("DATABASE_NAME", "this_is_not_correct")
    replicaset = os.getenv("MONGODB_REPLICASET", "rs0")

    if mock:
        import mongomock
        mongo_client = mongomock.MongoClient
    else:
        mongo_client = pymongo.MongoClient

    if replicaset:
        CLIENT = mongo_client("mongodb://{}:{}".format(host, port), replicaset="rs0")
    else:
        CLIENT = mongo_client("mongodb://{}:{}".format(host, port))
    DATABASE = CLIENT[database_name]


def get_database(mock=False):
    global DATABASE
    if DATABASE is None:
        connect(mock)
    return DATABASE


def get_client(mock=False):
    global CLIENT
    if CLIENT is None:
        connect(mock)
    return CLIENT
