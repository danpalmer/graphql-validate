"""
Checks on the structure of a GraphQL schema.
"""
from typing import Iterable

from graphql import (
    is_input_object_type,
    is_list_type,
    is_non_null_type,
    is_nullable_type,
    is_object_type,
)

from ..logging import logger
from .issues import TypeIssue

RELAY_FIELD_LIST_NAME = "edges"


def get_structural_issues(schema) -> Iterable[TypeIssue]:
    """Gets an iterable of structural issues with a schema."""

    logger.debug("Linting structure of schema")

    for type_name, type_ in schema.type_map.items():
        if is_object_type(type_) or is_input_object_type(type_):
            for field_name, field in type_.fields.items():
                if field_name == RELAY_FIELD_LIST_NAME:
                    continue

                possible_list_type = field.type

                if is_non_null_type(field.type):
                    possible_list_type = field.type.of_type

                if not is_list_type(possible_list_type):
                    continue

                if is_nullable_type(possible_list_type.of_type):
                    yield TypeIssue(
                        type_name=type_name,
                        type_issues=[],
                        field_issues={
                            field_name: ["Lists should not allow nullable elements."]
                        },
                    )
