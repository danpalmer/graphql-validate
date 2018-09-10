"""CLI handling for `graphql-validate`."""
import sys
import collections

import click
from graphql import GraphQLObjectType

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

    type_issues = collections.defaultdict(list)
    field_issues = collections.defaultdict(lambda: collections.defaultdict(list))

    logger.debug("Linting description fields in schema")

    for type_name, type_ in schema.type_map.items():
        logger.debug("Linting {name} description.".format(name=type_name))

        if type_.description is None:
            type_issues[type_name].append("Missing documentation")
        else:
            type_issues[type_name] = list(check_grammar(type_.description))

        if not isinstance(type_, GraphQLObjectType):
            continue

        for field_name, field in type_.fields.items():
            if field.description is None:
                field_issues[type_name][field_name].append("Missing documentation")
            else:
                field_issues[type_name][field_name] = list(
                    check_grammar(field.description)
                )

    num_issues = 0
    for type_name, doc_type_issues in sorted(type_issues.items()):
        if not doc_type_issues:
            continue

        click.echo(click.style("\n  " + type_name, fg="blue"))
        for issue in doc_type_issues:
            num_issues += 1
            click.echo("   - " + issue)

        if type_name not in field_issues:
            continue

        for field_name, doc_field_issues in field_issues[type_name].items():
            if not doc_field_issues:
                continue

            click.echo(click.style("\n     " + field_name, fg="blue"))
            for issue in doc_field_issues:
                num_issues += 1
                click.echo("      - " + issue)

    if type_issues:
        click.echo(
            click.style(
                "\n{num_issues} Issues detected".format(num_issues=num_issues), fg="red"
            )
        )
        sys.exit(1)
    else:
        click.echo(click.style("No issues detected.", fg="green"))
