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
"""Big int extension for graphene."""
from graphene.types import Scalar
from graphene.types.scalars import MAX_INT, MIN_INT
from graphql.language import ast


class BigInt(Scalar):
    """BigInt is an extension of the regular Int field.

    BigInt supports Integers bigger than a signed 32-bit integer.
    """

    @staticmethod
    def serializer(value):
        """Override the standard serializer to not raise exceptions on MAX_INT."""
        return int(value)

    serialize = serializer
    parse_value = serializer

    @staticmethod
    def parse_literal(node):
        """Parse node literal and convert to float if too large."""
        if isinstance(node, ast.IntValueNode):
            num = int(node.value)
            if num > MAX_INT or num < MIN_INT:
                return float(int(num))
            return num
        return None
