"""
Checks for the presence and validity of documentation.
"""

import collections
from typing import List, Mapping, NamedTuple

from graphql import GraphQLObjectType

from ..logging import logger

TypeIssue = NamedTuple(
    "TypeIssue",
    (
        ("type_name", str),
        ("type_issues", List[str]),
        ("field_issues", Mapping[str, List[str]]),
    ),
)


def get_documentation_issues(schema):
    """Get an iterable of documentation issues."""

    logger.debug("Linting description fields in schema")

    for type_name, type_ in schema.type_map.items():
        if type_name.startswith("__"):
            logger.debug("Skipping private type {name}.".format(name=type_name))
            continue

        logger.debug("Linting {name} description.".format(name=type_name))

        type_issues = []
        if type_.description is None:
            type_issues.append("Missing documentation")
        else:
            type_issues = list(check_grammar(type_.description))

        field_issues = collections.defaultdict(list)
        if isinstance(type_, GraphQLObjectType):
            for field_name, field in type_.fields.items():
                if field.description is None:
                    field_issues[field_name].append("Missing documentation")
                else:
                    field_issues[field_name] = list(check_grammar(field.description))

        if type_issues or field_issues:
            yield TypeIssue(
                type_name=type_name, type_issues=type_issues, field_issues=field_issues
            )


def check_grammar(text: str) -> [str]:
    """Return a list of human-readable issues with the given text."""
    if not text:
        yield "Empty documentation"
        return

    if text.strip() != text:
        yield "Documentation has leading/trailing whitespace."

    text = text.strip()

    if text[0] != text[0].upper():
        yield "Sentences should start with a capital letter."

    if text[-1] != ".":
        yield "Sentences should end with a full stop."