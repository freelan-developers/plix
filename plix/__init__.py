"""
Plix - A build matrix builder and runner.
"""

from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import compat  # noqa


# Add a new 'success' log level.
logging.SUCCESS = logging.INFO + 5
logging.addLevelName(logging.SUCCESS, 'SUCCESS')


def success(self, *args, **kwargs):
    """
    Log a success.

    >>> logging.getLogger().success("Hello")
    """
    return self.log(logging.SUCCESS, *args, **kwargs)

logging.Logger.success = success
