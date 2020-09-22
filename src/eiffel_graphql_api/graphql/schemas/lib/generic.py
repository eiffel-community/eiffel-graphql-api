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
"""Generic utilities for Eiffel GraphQL API."""
import json
import os
import re

import graphene

from .bigint import BigInt

BASE_JSON = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "events/json_schemas"
)

FIRST_CAPITAL_RE = re.compile("(.)([A-Z][a-z]+)")
ALL_CAPITAL_RE = re.compile("([a-z0-9])([A-Z])")


def convert(name):
    """Convert a javaCamelCase string to snake_case string.

    :param name: String to convert.
    :type name: str
    :return: Converted string.
    :rtype: str
    """
    # Since the first letter is lower-case the 'all_capital' regex won't function properly.
    # So we will instead do the first part separately.
    string = FIRST_CAPITAL_RE.sub(r"\1_\2", name)
    return ALL_CAPITAL_RE.sub(r"\1_\2", string).lower()


def load(name):
    """Load a json schema file from BASE_JSON path.

    :param name: Name of file to load.
    :type name: str
    :return: Json dictionary, starting from the properties key.
    :rtype: dict
    """
    with open(os.path.join(BASE_JSON, name)) as json_file:
        data = json.load(json_file)
    return data.get("properties")


def default_init(self, data):
    """Init function to use for generated ObjectTypes.

    This default __init__ is required to set the 'data' dictionary
    on all object types.
    The 'data' dictionary is either the full Eiffel event data object or
    a subset of it, depending on the level the ObjectType is on.

    If it's the 'data' key in GraphQL it's the full 'data' dictionary.
    If it's a sublevel (i.e data { customData }) key in GraphQL it will
    just be the 'customData' part.

    :param data: Eiffel event data dictionary.
    :type data: dict
    """
    self.data = data


class CustomData(graphene.ObjectType):
    """Custom data graphene object type.

    Due to graphene not being able to generate multiple objects with the same name, this
    generic CustomData object is created here and used in every event.
    """

    key = graphene.String()
    value = graphene.String()
    data = None

    def __init__(self, data):
        """Initialize with data.

        This is required for all eiffel graphql object types as we always
        get the return data from this data attribute.

        :param data: Eiffel event data dictionary.
                     Depending on the object type this can be either the full data object
                     or just a subset of it. In this case it's the subset for customData.
        :type data: dict
        """
        # pylint:disable=super-init-not-called
        self.data = data

    def resolve_key(self, _):
        """Resolve the 'key' part of customData."""
        return self.data.get("key")

    def resolve_value(self, _):
        """Resolve the 'value' part of customData."""
        return self.data.get("value")


def resolvers(graphene_type, data_key):
    """General resolver functions for the GraphQL API.

    Use this to get a resolver function for the graphene type you want to resolve.

    :param graphene_type: Graphene type.
    :type graphene_type: type
    :param data_key: Data key for the resolver to fetch.
    :type data_key: str
    :return: Resolver function for the graphene type.
    :rtype: function
    """

    def resolve_list(self, info):
        """Resolve a graphene list."""
        return [
            info.return_type.of_type.graphene_type(data)
            for data in self.data.get(data_key, [])
        ]

    def resolve_key(self, _):
        """Resolve a graphene dictionary."""
        if isinstance(self.data, dict):
            return self.data.get(data_key)
        return self.data

    def resolve_default(self, info):
        """Resolve a graphene key."""
        return info.return_type.graphene_type(self.data.get(data_key))

    _type = resolve_key
    if graphene_type == graphene.List:
        _type = resolve_list
    elif graphene_type == graphene.Field:
        _type = resolve_default
    return _type


def array_value(value):
    """Get the array values based on the json schema structure.

    :param value: Value to get 'value' from.
    :type value: dict
    :return: Dictionary which is parsable by 'generate_array'.
    :rtype: dict
    """
    if value.get("items").get("type") == "object":
        value = value.get("items").get("properties")
    elif value.get("items").get("type") == "string":
        value = {"type": {"type": "string"}}
    return value


def create_object_type(name, dictionary, key=None):
    """Create a graphene ObjectType.

    :param name: Name of the newly created ObjectType.
    :type name: str
    :param dictionary: Dictionary of methods to attach to ObjectType.
    :type dictionary: dict
    :param key: Key name for the object type. used to override 'customData'.
    :type key: str
    :return: Python object.
    :rtype: obj
    """
    if key == "customData":
        obj = CustomData
    else:
        obj = type(name, (graphene.ObjectType,), dictionary)
    return obj


def key_names(key, override_name):
    """Generate the different key names based on overrides and different naming schemes.

    :param key: Key to rename.
    :type key: str
    :param override_name: Overrides for key names.
                          Some eiffel keys have the same name and since graphene
                          cannot handle the same names of objects, we need to add
                          overrides for these.
    :type override_name: dict
    :return: Tuple of four different names:
             - Key name - with override if applicable (jsonCamelCase)
             - Data key - If key name is overriden, this will be the original (jsonCamelCase)
             - Cls name - Name of the class that should be generated (CamelCase)
             - attribute name - Name of the attribute (snake_case)
    :rtype: tuple
    """
    data_key = key
    key = override_name.get(key, key)
    # Capitalize removes the capital on the string. We only want the first letter
    # to change. By capitalizing just the first index and then attaching the rest
    # we achieve that.
    # Converts 'dataKey' to 'DataKey'.
    cls_name = "{}{}".format(key[0].capitalize(), key[1:])
    attribute_name = convert(key)
    return key, data_key, cls_name, attribute_name


def generate_array(key, value, override_name, data_dict):
    """Generate a graphene List for a json schema 'array'.

    Note that this function will also call the parent 'json_schema_to_graphql' which
    makes 'json_schema_to_graphql' a recursive function.
    This is because a json schema 'list' can have lists, simple objects or even
    complex objects inside it.

    :param key: Key name for this object.
    :type key: str
    :param value: Value to attach to the generated object.
    :type value: any
    :param override_name: Overrides for key names.
                          Some eiffel keys have the same name and since graphene
                          cannot handle the same names of objects, we need to add
                          overrides for these.
    :type override_name: dict
    :param data_dict: Dictionary to populate with the resolver as well as the generated object.
    :type data_dict: dict
    """
    key, data_key, cls_name, attribute_name = key_names(key, override_name)

    dictionary = {"__init__": default_init}
    value = array_value(value)
    json_schema_to_graphql(cls_name, value, dictionary, override_name)
    obj = create_object_type(cls_name, dictionary, key)
    data_dict[attribute_name] = graphene.List(obj)
    data_dict["resolve_{}".format(attribute_name)] = resolvers(graphene.List, data_key)


def generate_object(key, value, override_name, data_dict):
    """Generate a graphene Field for a json schema 'object'.

    Note that this function will also call the parent 'json_schema_to_graphql' which
    makes 'json_schema_to_graphql' a recursive function.
    This is because a json schema 'object' can have lists, simple objects or even
    complex objects inside it.

    :param key: Key name for this object.
    :type key: str
    :param value: Value to attach to the generated object.
    :type value: any
    :param override_name: Overrides for key names.
                          Some eiffel keys have the same name and since graphene
                          cannot handle the same names of objects, we need to add
                          overrides for these.
    :type override_name: dict
    :param data_dict: Dictionary to populate with the resolver as well as the generated object.
    :type data_dict: dict
    """
    key, data_key, cls_name, attribute_name = key_names(key, override_name)

    dictionary = {"__init__": default_init}
    json_schema_to_graphql(cls_name, value.get("properties"), dictionary, override_name)
    obj = create_object_type(cls_name, dictionary)
    data_dict[attribute_name] = graphene.Field(obj)
    data_dict["resolve_{}".format(attribute_name)] = resolvers(graphene.Field, data_key)


def generate_simple(key, graphene_type, override_name, data_dict):
    """Resolve simple keys.

    Will just create a graphene simple type and add a resolver to it.

    :param key: Key name for this object.
    :type key: str
    :param graphene_type: Graphene type object to use for the generated object.
    :type graphene_type: type
    :param override_name: Overrides for key names.
                          Some eiffel keys have the same name and since graphene
                          cannot handle the same names of objects, we need to add
                          overrides for these.
    :type override_name: dict
    :param data_dict: Dictionary to populate with the resolver as well as the generated object.
    :type data_dict: dict
    """
    key, _, __, attribute_name = key_names(key, override_name)
    data_dict[attribute_name] = graphene_type()
    data_dict["resolve_{}".format(attribute_name)] = resolvers(graphene_type, key)


def json_schema_to_graphql(
    name, data, data_dict=None, override_name={}
):  # pylint:disable=dangerous-default-value
    """Resolve an Eiffel JSONSchema and generate a GraphQL queryable structure.

    This function is quite complex in that it, in runtime, generates python objects
    that are used by graphene.

    Note that 'data_dict' is always passed along to the creators and they will
    populate it. Dictionaries are passed by reference.
    """
    if data_dict is None:
        data_dict = {}
    for key, value in data.items():
        if value.get("type") == "array":
            generate_array(key, value, override_name, data_dict)
        elif value.get("type") == "object":
            generate_object(key, value, override_name, data_dict)
        elif value.get("type") == "string":
            generate_simple(key, graphene.String, override_name, data_dict)
        elif value.get("type") == "integer":
            generate_simple(key, BigInt, override_name, data_dict)

    if data_dict:
        cls = type(
            name, (graphene.ObjectType,), {"__init__": default_init, **data_dict}
        )
        return graphene.Field(cls)
    return None
