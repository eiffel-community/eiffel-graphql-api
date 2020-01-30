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
import time
import pymongo
from eiffel_graphql_api.graphql.db.database import get_database
from eiffellib.subscribers.rabbitmq_subscriber import RabbitMQSubscriber

DATABASE = None

# Set environment variables from rabbitmq secrets in a kubernetes cluster.
if os.path.isfile("/etc/rabbitmq/password"):
    with open("/etc/rabbitmq/password", "r") as password:
        os.environ["RABBITMQ_PASSWORD"] = password.read()
if os.path.isfile("/etc/rabbitmq/username"):
    with open("/etc/rabbitmq/username", "r") as username:
        os.environ["RABBITMQ_USERNAME"] = username.read()


def insert_to_db(event, context):
    print(event)
    collection = DATABASE[event.meta.type]
    collection.create_index([("meta.id", pymongo.ASCENDING)])
    collection.create_index([("links.target", pymongo.ASCENDING)])
    doc = event.json
    doc['_id'] = event.meta.event_id
    try:
        collection.insert_one(doc)
    except pymongo.errors.DuplicateKeyError:
        print("Event already exists in the database, "
              "skipping: {}".format(event.json))
        return False
    return True


if __name__ == "__main__":
    DATABASE = get_database()
    SSL = os.getenv("RABBITMQ_SSL", "false") == "true"
    DATA = {
        "host": os.getenv("RABBITMQ_HOST", "127.0.0.1"),
        "exchange": os.getenv("RABBITMQ_EXCHANGE", "eiffel"),
        "username": os.getenv("RABBITMQ_USERNAME", None),
        "password": os.getenv("RABBITMQ_PASSWORD", None),
        "port": int(os.getenv("RABBITMQ_PORT", "5672")),
        "vhost": os.getenv("RABBITMQ_VHOST", None),
        "ssl": SSL,
        "queue": os.getenv("RABBITMQ_QUEUE", None),
        "routing_key": "#"
    }
    SUBSCRIBER = RabbitMQSubscriber(**DATA)
    SUBSCRIBER.subscribe("*", insert_to_db)
    SUBSCRIBER.start()

    while True:
        time.sleep(0.1)
