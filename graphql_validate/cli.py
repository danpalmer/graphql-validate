"""CLI handling for `graphql-validate`."""
import sys
import collections

import click

from graphql_validate.grammar import check_grammar
from graphql_validate.logging import logger, set_verbosity
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

    issues = collections.defaultdict(list)
    logger.debug("Linting description fields in schema")

    for type_name, type_ in schema.type_map.items():
        logger.debug("Linting {name} description.".format(name=type_name))

        if type_.description is None:
            issues[type_name].append("Missing documentation")
        else:
            issues[type_name] = list(check_grammar(type_.description))

    for type_name, doc_issues in sorted(issues.items()):
        if not doc_issues:
            continue
        click.echo(click.style("\n  " + type_name, fg="blue"))
        for issue in doc_issues:
            click.echo("   - " + issue)

    if issues:
        click.echo(click.style("\nIssues detected.", fg="red"))
        sys.exit(1)
    else:
        click.echo(click.style("No issues detected.", fg="green"))
