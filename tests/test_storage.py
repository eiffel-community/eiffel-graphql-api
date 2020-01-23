# Copyright 2020 Axis Communications AB.
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
# -*- coding: utf-8 -*-

from eiffellib.events.eiffel_composition_defined_event import EiffelCompositionDefinedEvent

from eiffel_graphql_api import storage
from eiffel_graphql_api.graphql.db.database import get_database


def test_storage_insert_single_doc():
    storage.DATABASE = get_database(True)
    event = EiffelCompositionDefinedEvent()

    assert storage.insert_to_db(event, None)
    collection = storage.DATABASE[event.meta.type]
    result = collection.find_one({"_id": event.meta.event_id})
    del result["_id"]
    assert result == event.json


def test_storage_ignores_duplicate_ids():
    storage.DATABASE = get_database(True)
    event = EiffelCompositionDefinedEvent()

    assert storage.insert_to_db(event, None)
    assert not storage.insert_to_db(event, None)
