"""Helper functions"""
from dataclasses import fields
from enum import EnumType
from typing import Union, get_origin, get_args, Any

SCHEMA_TYPE_MAPPING = {
    str: {"type": "string"},
    int: {"type": "integer"},
    float: {"type": "number"},
    bool: {"type": "boolean"},
}


def infer_type_from_enum(enum_class):
    """
    Generates an OpenAPI schema from an enum class.
    """
    schema = {"type": "string", "enum": [member.value for member in enum_class]}
    if isinstance(next(iter(enum_class)), int):
        schema["type"] = "integer"
    return schema

def to_schema(dtcls: Any) -> dict:
    """
    Converts a dataclass type to an OpenAPI Schema.
    This can be used for building ChatGPT functions.

    :param dtcls: The dataclass type to convert.
    :return: The OpenAPI schema representing the dataclass type.
    """
    if dtcls in SCHEMA_TYPE_MAPPING:
        return SCHEMA_TYPE_MAPPING[dtcls]
    if isinstance(dtcls, EnumType):
        return infer_type_from_enum(dtcls)

    schema = {"type": "object", "properties": {}}

    for field in fields(dtcls):
        field_type = field.type
        if get_origin(field_type) == Union:
            field_type = get_args(field_type)[0]
        field_name = field.name

        if get_origin(field_type) == list:
            schema["properties"][field_name] = {
                "type": "array",
                "items": to_schema(get_args(field_type)[0]),
            }
        elif get_origin(field_type) == dict:
            schema["properties"][field_name] = {
                "type": "object",
                "additionalProperties": to_schema(get_args(field_type)[1]),
            }
        elif hasattr(field_type, "__annotations__"):
            schema["properties"][field_name] = to_schema(field_type)
        else:
            schema["properties"][field_name] = to_schema(field_type)
    return schema
