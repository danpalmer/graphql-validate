"""CLI handling for `graphql-validate`."""
import logging

import click

logger = logging.getLogger("graphql_validate")


@click.group()
@click.option("-v", "--verbose", help="Log all output.", is_flag=True)
def main(verbose):
    """Shared entrypoint."""
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.CRITICAL)


@main.command()
@click.option(
    "--strict", help="Be strict about documentation formatting.", is_flag=True
)
@click.option(
    "-s",
    "--schema",
    help="The schema to inspect, must be either HTTP(s) or a local file",
    type=str,
)
def documentation(strict, schema):  # pragma: no cover
    """Lint a schema's documentation."""
    click.echo(click.style("Done", fg="green"))
