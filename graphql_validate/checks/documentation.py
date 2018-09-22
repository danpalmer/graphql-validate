"""
Checks for the presence and validity of documentation.
"""

import collections
from typing import Iterable, Optional, TYPE_CHECKING

from graphql import is_object_type

from ..logging import logger
from .issues import TypeIssue

if TYPE_CHECKING:
    from typing import List, Mapping  # noqa: F401


def get_documentation_issues(schema) -> Iterable[TypeIssue]:
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

        field_issues = collections.defaultdict(list)  # type: Mapping[str, List[str]]
        if is_object_type(type_):
            for field_name, field in type_.fields.items():
                if not field.description:
                    field_issues[field_name].append("Missing documentation")

                field_issues[field_name].extend(list(check_grammar(field.description)))

                if field.is_deprecated:
                    if not field.deprecation_reason:
                        field_issues[field_name].append("Missing deprecation reason")

                    field_issues[field_name].extend(
                        list(check_grammar(field.deprecation_reason))
                    )

        if type_issues or any(field_issues.values()):
            yield TypeIssue(
                type_name=type_name, type_issues=type_issues, field_issues=field_issues
            )


def check_grammar(text: Optional[str]) -> Iterable[str]:
    """Return a list of human-readable issues with the given text."""
    if not text:
        return

    if text.strip() != text:
        yield "Documentation has leading/trailing whitespace."

    text = text.strip()

    if text[0] != text[0].upper():
        yield "Sentences should start with a capital letter."

    if text[-1] != ".":
        yield "Sentences should end with a full stop."
