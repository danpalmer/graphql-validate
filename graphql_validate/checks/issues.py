"""
Core type for check output.
"""

from typing import List, Mapping, NamedTuple

TypeIssue = NamedTuple(
    "TypeIssue",
    (
        ("type_name", str),
        ("type_issues", List[str]),
        ("field_issues", Mapping[str, List[str]]),
    ),
)
