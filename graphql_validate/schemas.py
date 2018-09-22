"""Resolution of schema arguments into schema objects."""

import json
from typing import Optional

import click
import requests
from graphql import build_client_schema, get_introspection_query, GraphQLSchema

from graphql_validate.logging import logger


def resolve_schema_cli(ctx, param, value):
    """Given a string path/URL to a schema, turn it into a schema object."""

    try:
        if value.startswith("http"):
            return _resolve_url(ctx, value)

        with open(value, "rb") as f:
            filecontents = f.read().decode("utf-8")

        try:
            json.loads(filecontents)
            is_json = True
        except json.decoder.JSONDecodeError:
            is_json = False

        if is_json:
            return _resolve_json(ctx, filecontents)

        return _resolve_sdl(ctx, filecontents)

    except ValueError as e:
        logger.exception(e)
        raise click.BadParameter(str(e))
    except IOError as e:
        logger.exception(e)
        raise click.BadParameter(
            "Could not read file '{filename}'".format(filename=value)
        )


def _resolve_url(ctx, url: str) -> Optional[GraphQLSchema]:
    query = get_introspection_query(descriptions=True)

    try:
        response = requests.post(
            url, data={"query": query}, headers={"Accept": "application/json"}
        )
        response.raise_for_status()
    except requests.RequestException:
        raise ValueError("Could not download schema")

    try:
        data = response.json()
    except json.decoder.JSONDecodeError:
        raise ValueError("Received invalid JSON from GraphQL endpoint")

    try:
        return build_client_schema(data["data"])
    except Exception:
        raise ValueError("Could not decode schema")


def _resolve_sdl(ctx, filecontents: str) -> Optional[GraphQLSchema]:
    pass


def _resolve_json(ctx, filecontents: str) -> Optional[GraphQLSchema]:
    pass
