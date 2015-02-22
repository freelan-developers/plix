"""
Command-line entry point.
"""

from __future__ import print_function

import argparse
import logging
import sys
import yaml

from chromalog import basicConfig

from .configuration import Configuration


def main():
    logger = logging.getLogger('plix')
    basicConfig(format='%(message)s', level=logging.INFO)

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
        type=Configuration.load_from_file,
        help="The configuration file to use.",
    )

    try:
        args = parser.parse_args()
    except Exception as ex:
        logger.error("%s", ex)
        sys.exit(1)

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled.")
        logger.debug(
            "Parsed configuration is shown below:\n\n%s\n",
            yaml.safe_dump(args.configuration.conf, indent=2),
        )
