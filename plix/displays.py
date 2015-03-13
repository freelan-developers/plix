"""
Display command results.
"""

from __future__ import unicode_literals

from contextlib import contextmanager
from argparse import Namespace
from io import BytesIO

from colorama import AnsiToWin32

from chromalog.stream import stream_has_color_support
from chromalog.colorizer import Colorizer
from chromalog.mark.helpers.simple import (
    warning,
    important,
    success,
    error,
)


class BaseDisplay(object):
    """
    Provides general display logic to its subclasses.
    """

    @contextmanager
    def command(self, index, command):
        """
        Contextmanager that wraps calls to :func:`start_command` and
        :func:`stop_command`.

        :param index: The index of the command.
        :param command: The command that is about to be executed, as an unicode
            string.
        """

        self.start_command(
            index=index,
            command=command,
        )

        result = Namespace(returncode=None)

        try:
            yield result
        finally:
            self.stop_command(
                index=index,
                command=command,
                returncode=result.returncode,
            )


class StreamDisplay(BaseDisplay):
    """
    Displays commands output to an output stream.
    """

    def __init__(self, stream, colorizer=Colorizer()):
        """
        Initialize the :class:`StreamDisplay`.

        :param stream: The stream to be attached too.
        """
        super(StreamDisplay, self).__init__()
        self.colorizer = colorizer
        self.output_map = {}

        if stream_has_color_support(stream):
            self.stream = AnsiToWin32(stream).stream
        else:
            self.stream = stream

        # Python 3 differentiates binary streams.
        if hasattr(stream, 'buffer'):
            self.binary_stream = stream.buffer
        else:
            self.binary_stream = stream

    def format_output(self, message, *args, **kwargs):
        """
        Format some output in regards to the output stream color-capability.

        :param message: A message.
        :returns: The formatted message.
        """
        if stream_has_color_support(self.stream):
            return self.colorizer.colorize_message(message, *args, **kwargs)
        else:
            return message.format(*args, **kwargs)

    def set_context(self, commands):
        """
        Set the context for display.

        :param commands: The list of commands to be executed.
        """
        self.longest_len = max(map(len, commands))

    def start_command(self, index, command):
        """
        Indicate that a command stopped.

        :param index: The index of the command.
        :param command: The command that is about to be executed, as an unicode
            string.
        """
        self.stream.write(self.format_output(
            "{}) {}",
            warning(important(index + 1)),
            command,
        ))
        self.stream.flush()
        self.output_map[index] = BytesIO()

    def stop_command(self, index, command, returncode):
        """
        Indicate that a command stopped.

        :param index: The index of the command.
        :param command: The command that was executed, as an unicode string.
        :param returncode: The exit status.
        """
        self.stream.write(self.format_output(
            "{}\t[{}]\n",
            " " * (self.longest_len - len(command)),
            success("success") if returncode == 0 else error("failed"),
        ))

        if returncode != 0:
            self.binary_stream.write(self.output_map[index].getvalue())
            self.stream.write(self.format_output(
                "{}) {} {}\n",
                warning(important(index + 1)),
                error("Command exited with"),
                important(error(returncode)),
            ))

        del self.output_map[index]

    def command_output(self, index, data):
        """
        Add some output for a command.

        :param index: The index of the command.
        :param data: The output data (as bytes).
        """
        self.output_map[index].write(data)
