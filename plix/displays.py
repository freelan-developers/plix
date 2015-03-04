"""
Display command results.
"""

from __future__ import unicode_literals

from contextlib import contextmanager
from argparse import Namespace


class BaseDisplay(object):
    """
    Provides general display logic to its subclasses.
    """

    @contextmanager
    def command(self, index, total, command):
        """
        Contextmanager that wraps calls to :func:`start_command` and
        :func:`stop_command`.

        :param index: The index of the command.
        :param total: The total number of commands.
        :param command: The command that is about to be executed, as an unicode
            string.
        """

        self.start_command(
            index=index,
            total=total,
            command=command,
        )

        result = Namespace(returncode=None)

        try:
            yield result
        finally:
            self.stop_command(
                index=index,
                total=total,
                command=command,
                returncode=result.returncode,
            )


class StreamDisplay(BaseDisplay):
    """
    Displays commands output to an output stream.
    """

    def __init__(self, stream):
        """
        Initialize the :class:`StreamDisplay`.

        :param stream: The stream to be attached too.
        """
        super(StreamDisplay, self).__init__()
        self.stream = stream

        # Python 3 differentiates binary streams.
        if hasattr(stream, 'buffer'):
            self.binary_stream = stream.buffer
        else:
            self.binary_stream = stream

    def start_command(self, index, total, command):
        """
        Indicate that a command stopped.

        :param index: The index of the command.
        :param total: The total number of commands.
        :param command: The command that is about to be executed, as an unicode
            string.
        """
        self.stream.write("> {}\n".format(command))

    def stop_command(self, index, total, command, returncode):
        """
        Indicate that a command stopped.

        :param index: The index of the command.
        :param total: The total number of commands.
        :param command: The command that was executed, as an unicode string.
        :param returncode: The exit status.
        """
        self.stream.write("> Exit status: {}\n".format(returncode))

    def command_output(self, index, data):
        """
        Add some output for a command.

        :param index: The index of the command.
        :param data: The output data (as bytes).
        """
        self.binary_stream.write(data)
