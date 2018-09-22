"""CLI handling for `graphql-validate`."""
import sys
from typing import Iterable

import click

from graphql_validate.checks import (
    get_documentation_issues,
    get_structural_issues,
    TypeIssue,
)
from graphql_validate.logging import set_verbosity
from graphql_validate.schemas import resolve_schema_cli

verbosity = click.option(
    "-v", "--verbose", help="Log all output.", is_flag=True, callback=set_verbosity
)


@click.group()
def cli():
    """Main entrypoint."""


@cli.command()
@verbosity
@click.argument("schema", callback=resolve_schema_cli)
def documentation(schema, verbose):  # pragma: no cover
    """Lint a schema's documentation."""
    _print_issues(get_documentation_issues(schema))


@cli.command()
@verbosity
@click.argument("schema", callback=resolve_schema_cli)
def structure(schema, verbose):  # pragma: no cover
    """Lint a schema's structure."""
    _print_issues(get_structural_issues(schema))


def _print_issues(issues: Iterable[TypeIssue]):
    num_issues = 0
    for type_issue in sorted(issues, key=lambda x: x.type_name):
        click.echo(click.style("\n  " + type_issue.type_name, fg="blue"))
        for issue in type_issue.type_issues:
            num_issues += 1
            click.echo("   - " + issue)

        for field_name, field_issues in sorted(type_issue.field_issues.items()):
            for field_issue in field_issues:
                num_issues += 1
                click.echo(
                    "   - {0}: {1}".format(
                        click.style(field_name, fg="yellow"), field_issue
                    )
                )

    if issues:
        click.echo(
            click.style(
                "\n  {num_issues} Issues detected\n".format(num_issues=num_issues),
                fg="red",
            )
        )
        sys.exit(1)
    else:
        click.echo(click.style("No issues detected.", fg="green"))
