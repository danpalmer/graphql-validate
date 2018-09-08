"""Shared logger setup."""

import logging

logger = logging.getLogger("graphql-validate")


def set_verbosity(ctx, param, verbose):
    """Set the verbosity level from the CLI."""

    level = logging.DEBUG if verbose else logging.CRITICAL
    logging.basicConfig(level=level, format="%(message)s")
    logger.debug("Logging is set to {level}".format(level=level))
    return verbose
