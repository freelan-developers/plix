"""
Command-line entry point.
"""

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import sys
import pkg_resources

from chromalog import basicConfig
from chromalog.mark.helpers.simple import (
    important,
    debug,
)

from .configuration import load_from_file
from .log import logger
from .compat import yaml_dump
from .commands import (
    command_run,
)
from .exceptions import (
    DuplicateKeys,
    UnknownKeys,
)


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

    command_parser = parser.add_subparsers(help='The available commands.')

    # The run command
    run_command_parser = command_parser.add_parser(
        'run',
        help='Run the matrix.',
    )
    run_command_parser.set_defaults(
        command=command_run,
        command_args={'configuration', 'pairs'},
    )
    run_command_parser.add_argument(
        'pairs',
        nargs='*',
        default=[],
        action=PairsParser,
        help="A list of matrix context pairs that to limit the run to.",
    )

    try:
        return parser.parse_args(args)
    except Exception as ex:
        logger.error("%s", ex)
        raise SystemExit(1)


def extract_command_and_args(params):
    command = params.command
    command_args = params.command_args

    return command, {
        arg: getattr(params, arg)
        for arg in command_args
    }


def main(args=sys.argv[1:]):
    basicConfig(format='%(message)s', level=logging.INFO)
    params = parse_args(args=args)

    logger.info(
        "This is %s version %s. Prepare to be amazed !\n",
        debug(important("plix")),
        debug(important(pkg_resources.get_distribution("plix").version)),
    )

    if params.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled.")
        logger.debug(
            "Parsed configuration is shown below:\n\n%s\n",
            yaml_dump(params.configuration, indent=2),
        )

    command, args = extract_command_and_args(params)

    try:
        command(logger=logger, **args)
    except DuplicateKeys as ex:
        logger.error(
            "Duplicated keys are not allowed in the configuration (keys: %s).",
            important(", ".join(ex.keys)),
        )
    except UnknownKeys as ex:
        logger.error(
            "Unable to parse the configuration. Some keys are unknown: %s",
            important(", ".join(ex.keys)),
        )
    except Exception as ex:
        if not params.debug:
            logger.error("%s", ex)
            raise SystemExit(1)
        else:
            raise
