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
"""DB Storage tool for eiffel graphql API."""
import argparse
import logging
import os
import sys
import time

from eiffellib.subscribers.rabbitmq_subscriber import RabbitMQSubscriber

from eiffel_graphql_api import __version__
from eiffel_graphql_api.graphql.db.database import insert_to_db

LOGGER = logging.getLogger(__name__)

# Set environment variables from rabbitmq secrets in a kubernetes cluster.
if os.path.isfile("/etc/rabbitmq/password"):
    with open("/etc/rabbitmq/password", "r") as password:
        os.environ["RABBITMQ_PASSWORD"] = password.read()
if os.path.isfile("/etc/rabbitmq/username"):
    with open("/etc/rabbitmq/username", "r") as username:
        os.environ["RABBITMQ_USERNAME"] = username.read()


def parse_args(args):
    """Parse command line parameters.

    :param args: Command line parameters as list of strings.
    :type args: list
    :return: Command line parameters namespace.
    :rtype: :obj:`argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description="Tool for storing eiffel events in a Mongo database."
    )
    parser.add_argument(
        "--version",
        action="version",
        version="eiffel-graphql-storage {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        default=logging.INFO,
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Set up basic logging.

    :param loglevel: Minimum loglevel for emitting messages.
    :type loglevel: int
    """
    logformat = "[%(asctime)s] %(levelname)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Start GraphQL storage tool, connect to MongoDB and subscribe to Eiffel.

    :param args: Input arguments to storage tool.
    :type args: list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    ssl = os.getenv("RABBITMQ_SSL", "false") == "true"
    data = {
        "host": os.getenv("RABBITMQ_HOST", "127.0.0.1"),
        "exchange": os.getenv("RABBITMQ_EXCHANGE", "eiffel"),
        "username": os.getenv("RABBITMQ_USERNAME", None),
        "password": os.getenv("RABBITMQ_PASSWORD", None),
        "port": int(os.getenv("RABBITMQ_PORT", "5672")),
        "vhost": os.getenv("RABBITMQ_VHOST", None),
        "ssl": ssl,
        "queue": os.getenv("RABBITMQ_QUEUE", None),
        "routing_key": "#",
    }
    subscriber = RabbitMQSubscriber(**data)
    subscriber.subscribe("*", insert_to_db, can_nack=True)
    subscriber.start()

    while True:
        time.sleep(0.1)


def run():
    """Entry point for console_scripts."""
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
