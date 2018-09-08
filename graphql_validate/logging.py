"""Shared logger setup."""

import logging

logger = logging.getLogger("graphql-validate")


def set_verbosity(ctx, param, verbose):
    """Set the verbosity level from the CLI."""

    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.CRITICAL)
    return verbose
