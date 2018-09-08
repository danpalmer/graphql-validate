"""CLI handling for `graphql-validate`."""
import click

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
@click.option(
    "--strict", help="Be strict about documentation formatting.", is_flag=True
)
@click.argument("schema", callback=resolve_schema_cli)
def documentation(strict, schema, verbose):  # pragma: no cover
    """Lint a schema's documentation."""
    click.echo(click.style("Done", fg="green"))
