"""
Matrix utilities.
"""

from __future__ import unicode_literals

from itertools import product

from jinja2 import (
    Environment,
    meta,
)

from .exceptions import UnknownKeys


def find_required_keys(*commands):
    """
    Parse a command and get a set of all referenced context keys it contains.

    :param commands: The command(s) to parse.
    :returns: A set of all contained context keys.
    """
    result = set()

    for command in commands:
        result |= meta.find_undeclared_variables(Environment().parse(command))

    return result


def generate_variants(matrix, subset_pairs=set()):
    """
    Generate all variants for the specified ``matrix``, eventually limiting to
    those that contain ``subset_pairs``.

    :param matrix: The matrix to generate the variants from.
    :param subset_pairs: A set of pairs that limits the generated matrices.
    :yields: Sets of pairs for each of the matrix variants.
    """
    keys = frozenset(matrix.keys())
    subset_pairs = frozenset(subset_pairs)

    for values in product(
            *[value for key, value in sorted(matrix.items()) if key in keys]
    ):
        variant = frozenset(zip(sorted(keys), values))

        if subset_pairs.issubset(variant):
            yield variant


def validate_keys(matrix, keys):
    """
    Validate that all ``keys`` are dimensions in ``matrix``.

    :param matrix: The matrix to validate into.
    :param keys: The keys to validate.
    :returns: The matrix, limited to its ``keys`` dimensions.
    """
    keys = frozenset(keys)
    mkeys = frozenset(matrix.keys())
    unknown_keys = keys.difference(mkeys)

    if unknown_keys:
        raise UnknownKeys(keys=unknown_keys)

    return {
        key: value
        for key, value in matrix.items()
        if key in keys
    }
