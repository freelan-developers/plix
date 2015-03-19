"""
Matrix utilities.
"""

from __future__ import unicode_literals

from six import string_types

from itertools import product

from jinja2 import (
    Environment,
    meta,
    Template,
)


def find_required_keys(objects):
    """
    Parse objects nd and get a set of all referenced context keys they contain.

    :param objects: The objects to parse.
    :returns: A set of all contained context keys.
    """
    result = set()

    for obj in objects:
        if isinstance(obj, string_types):
            result |= meta.find_undeclared_variables(Environment().parse(obj))
        elif isinstance(obj, (list, tuple)):
            result |= find_required_keys(obj)
        elif isinstance(obj, dict):
            result |= find_required_keys(obj.items())

    return result


def render_object(obj, context):
    """
    Render an object with the specified `context`.

    :param obj: The object to render.
    :param context: The context to use.
    :returns: The rendered object.
    """
    if isinstance(obj, string_types):
        return Template(obj).render(**context)
    elif isinstance(obj, (list, tuple)):
        return type(obj)(render_object(x, context) for x in obj)
    elif isinstance(obj, dict):
        return {
            key: render_object(value, context)
            for key, value in obj.items()
        }
    else:
        return obj


def generate_variants(matrix):
    """
    Generate all variants for the specified ``matrix``.

    :param matrix: The matrix to generate the variants from.
    :returns: Sets of pairs for each of the matrix variants.
    """
    keys = frozenset(matrix.keys())
    variants = []

    for values in product(
            *[value for key, value in sorted(matrix.items()) if key in keys]
    ):
        variants.append(frozenset(zip(sorted(keys), values)))

    return variants


def filter_variants(variants, subset_pairs):
    """
    Filter variants that don't contain the specified subset_pairs.

    :param subset_pairs: A set of pairs that limits the generated matrices.
    :returns: The variants that contain the specified `subset_pairs`.
    """
    subset_pairs = frozenset(subset_pairs)

    return [
        variant
        for variant in variants
        if subset_pairs.issubset(variant)
    ]


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

    return {
        key: value
        for key, value in matrix.items()
        if key in keys
    }, unknown_keys
