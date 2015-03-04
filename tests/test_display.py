"""
Test the displays.
"""

from __future__ import unicode_literals

from unittest import TestCase
from mock import MagicMock

from plix.displays import (
    BaseDisplay,
    StreamDisplay,
)


class DisplaysTests(TestCase):
    def test_base_display_command_context_manager(self):
        class MyDisplay(BaseDisplay):
            start_command = MagicMock()
            stop_command = MagicMock()

        my_display = MyDisplay()

        with my_display.command(42, 1984, "my command") as result:
            result.returncode = 1234

        my_display.start_command.assert_called_once_with(
            index=42,
            total=1984,
            command="my command",
        )
        my_display.stop_command.assert_called_once_with(
            index=42,
            total=1984,
            command="my command",
            returncode=1234,
        )

    def test_stream_display_handles_binary_streams_py2(self):
        stream = MagicMock()
        del stream.buffer
        display = StreamDisplay(stream=stream)

        self.assertEqual(display.stream, stream)
        self.assertEqual(display.binary_stream, stream)

    def test_stream_display_handles_binary_streams_py3(self):
        stream = MagicMock()
        display = StreamDisplay(stream=stream)

        self.assertEqual(display.stream, stream)
        self.assertEqual(display.binary_stream, stream.buffer)

    def test_stream_display_start_command(self):
        stream = MagicMock()
        display = StreamDisplay(stream=stream)
        display.start_command(42, 1984, "my command")

        stream.write.assert_called_once_with("> my command\n")

    def test_stream_display_stop_command(self):
        stream = MagicMock()
        display = StreamDisplay(stream=stream)
        display.stop_command(42, 1984, "my command", 1234)

        stream.write.assert_called_once_with("> Exit status: 1234\n")

    def test_stream_display_command_output_py2(self):
        stream = MagicMock()
        del stream.buffer
        display = StreamDisplay(stream=stream)
        data = "DATA".encode('utf-8')
        display.command_output(42, data)

        stream.write.assert_called_once_with(data)

    def test_stream_display_command_output_py3(self):
        stream = MagicMock()
        display = StreamDisplay(stream=stream)
        data = "DATA".encode('utf-8')
        display.command_output(42, data)

        stream.buffer.write.assert_called_once_with(data)
