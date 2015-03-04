"""
Command-line entry point.
"""

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import sys
import yaml
import os

from chromalog import basicConfig

from .configuration import load_from_file
from .log import logger
from .displays import StreamDisplay
from .compat import yaml_dump


class PairsParser(argparse.Action):
    """
    Parses pairs of `key:value` arguments.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        pairs = []

        for value in values:
            if ':' not in value:
                raise ValueError(
                    "{} does not respect the `key:value` format".format(value),
                )

            pairs.append(tuple(value.split(':', 2)))

        setattr(namespace, self.dest, frozenset(pairs))


def parse_args(args):
    """
    Parse the arguments.

    :param args: The arguments to parse.
    :returns: A namespace instance.
    """
    parser = argparse.ArgumentParser(
        description="Plix - a build matrix runner that cares about humans.",
    )
    parser.add_argument(
        '--debug',
        '-d',
        action='store_true',
        default=False,
        help="Enable debug output.",
    )
    parser.add_argument(
        '--configuration',
        '-c',
        default='.plix.yml',
        type=load_from_file,
        help="The configuration file to use.",
    )
    parser.add_argument(
        'pairs',
        nargs='*',
        default=[],
        action=PairsParser,
        help="A list of matrix context pairs that will limit the build.",
    )

    try:
        return parser.parse_args(args)
    except Exception as ex:
        logger.error("%s", ex)
        raise SystemExit(1)


def main(args=sys.argv[1:]):
    basicConfig(format='%(message)s', level=logging.INFO)
    params = parse_args(args=args)

    if params.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled.")
        logger.debug(
            "Parsed configuration is shown below:\n\n%s\n",
            yaml_dump(params.configuration, indent=2),
        )

    display = StreamDisplay(stream=sys.stdout)

    params.configuration['executor'].execute(
        environment=os.environ,
        commands=params.configuration['script'],
        display=display,
    )
