"""
Plix - A build matrix builder and runner.
"""

import logging


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
