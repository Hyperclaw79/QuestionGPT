"""Helper functions"""
from dataclasses import fields, dataclass
from typing import Union, get_origin, get_args

def extract_fields(dtcls: dataclass) -> dict:
    """
    Extracts the mandatory and optional fields from a dataclass type.

    :param dtcls: The dataclass type to extract fields from.
    :return: A dict of the mandatory and optional fields.
    """
    mandatory = []
    optional = []
    for field in fields(dtcls):
        if get_origin(field.type) == Union and get_args(field.type)[1] is type(None):
            optional.append(field.name)
            continue
        mandatory.append(field.name)
    return {"mandatory": mandatory, "optional": optional}
