"""
Main entry point for `graphql-validate` command-line utility.

This is to enable `python -m graphql-validate` if that is needed for any reason,
normal use should be to use the `graphql-validate` command-line tool directly.
"""

from graphql_validate.cli import cli

cli()
