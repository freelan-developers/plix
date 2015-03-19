"""
The commands.
"""

import os
import sys

from .displays import StreamDisplay
from .matrix import (
    find_required_keys,
    validate_keys,
    generate_variants,
    filter_variants,
    render_object,
)
from .exceptions import (
    DuplicateKeys,
    UnknownKeys,
)

from chromalog.mark.helpers.simple import important


def find_required_keys_in_configuration(configuration):
    """
    Get the required keys from the specified `configuration`.

    :params configuration: The configuration.
    :returns: The required keys.
    """
    return find_required_keys([
        configuration[key] for key in {
            'global',
            'install',
            'script',
            'after_success',
            'after_failure',
        }
    ])


def get_context(variant, configuration):
    """
    Get the context out of the `variant` and `configuration`.
    """
    context = dict(variant)
    context.update(render_object(configuration['global'], context))

    return context


def run_variant(logger, display, variant, configuration):
    """
    Run a matrix variant.
    """
    logger.info(
        "> Running variant %s.",
        important(",".join(
            "{}:{}".format(key, value) for key, value in sorted(variant)
        )),
    )

    context = get_context(variant, configuration)
    commands = [render_object(obj, context) for obj in configuration['script']]

    return configuration['executor'].execute(
        environment=os.environ,
        commands=commands,
        display=display,
    )


def command_run(
    logger,
    configuration,
    pairs,
    display=StreamDisplay(stream=sys.stdout),
):
    """
    Run the matrix.
    """
    full_matrix = configuration['matrix']
    global_keys = frozenset(configuration['global'])
    required_keys = find_required_keys_in_configuration(configuration)
    matrix, unknown_keys = validate_keys(matrix=full_matrix, keys=required_keys)
    unreferenced_keys = set(full_matrix).difference(set(matrix)).union(
        global_keys.difference(unknown_keys),
    )
    variants = generate_variants(matrix)
    filtered_variants = filter_variants(variants, pairs)
    unknown_keys = unknown_keys - global_keys
    duplicate_keys = global_keys.intersection(full_matrix)

    if duplicate_keys:
        raise DuplicateKeys(duplicate_keys)

    if unknown_keys:
        raise UnknownKeys(unknown_keys)

    if unreferenced_keys:
        logger.warning(
            "The following key(s) is/are never referenced: %s. You might want "
            "to consider removing it/them from the configuration file.",
            important(", ".join(unreferenced_keys)),
        )

    logger.debug(
        "Matrix has %d dimension(s), %d variant(s).",
        len(matrix),
        len(variants),
    )

    if filtered_variants != variants:
        logger.info(
            "About to run %d out of %d variants...",
            len(filtered_variants),
            len(variants),
        )
    else:
        logger.info(
            "About to run all %d variants...",
            len(filtered_variants),
        )

    for variant in filtered_variants:
        if not run_variant(
            logger=logger,
            display=display,
            variant=variant,
            configuration=configuration,
        ):
            logger.error("Last variant failed: build interrupted.")
            break
