"""
Test the displays.
"""

from __future__ import unicode_literals

from unittest import TestCase
from mock import (
    MagicMock,
    patch,
    call,
)
from chromalog.colorizer import GenericColorizer

from plix.displays import (
    BaseDisplay,
    StreamDisplay,
)


class DisplaysTests(TestCase):
    def test_base_display_command_context_manager(self):
        class MyDisplay(BaseDisplay):
            start_command = MagicMock()
            stop_command = MagicMock()

        display = MyDisplay()

        with display.command(42, "my command") as result:
            result.returncode = 1234

        display.start_command.assert_called_once_with(
            index=42,
            command="my command",
        )
        display.stop_command.assert_called_once_with(
            index=42,
            command="my command",
            returncode=1234,
        )

    def test_stream_display_py2_no_color(self):
        stream = MagicMock()
        del stream.isatty
        del stream.buffer
        display = StreamDisplay(stream=stream)
        display.set_context(commands=["my command"])

        self.assertEqual(stream, display.stream)
        self.assertEqual(stream, display.binary_stream)

        with display.command(42, "my command") as result:
            data = "DATA".encode('utf-8')
            display.command_output(42, data)
            result.returncode = 17

        self.assertEqual(
            [
                call("43) my command"),
                call("\t[failed]\n"),
                call(data),
                call("43) Command exited with 17\n"),
            ],
            stream.write.mock_calls,
        )

    def test_stream_display_py3_no_color(self):
        stream = MagicMock()
        del stream.isatty
        display = StreamDisplay(stream=stream)
        display.set_context(commands=["my command"])

        self.assertEqual(stream, display.stream)
        self.assertEqual(stream.buffer, display.binary_stream)

        with display.command(42, "my command") as result:
            data = "DATA".encode('utf-8')
            display.command_output(42, data)
            result.returncode = 17

        self.assertEqual(
            [
                call("43) my command"),
                call("\t[failed]\n"),
                call("43) Command exited with 17\n"),
            ],
            stream.write.mock_calls,
        )
        stream.buffer.write.assert_called_once_with(data)

    @patch('plix.displays.AnsiToWin32')
    def test_stream_display_py2_with_color(self, AnsiToWin32):
        stream = MagicMock()
        del stream.buffer
        colorizer = GenericColorizer(color_map={
            'error': ('<', '>'),
            'warning': ('(', ')'),
        })
        display = StreamDisplay(stream=stream, colorizer=colorizer)
        display.set_context(commands=["my command"])

        self.assertEqual(AnsiToWin32().stream, display.stream)
        self.assertEqual(stream, display.binary_stream)

        with display.command(42, "my command") as result:
            data = "DATA".encode('utf-8')
            display.command_output(42, data)
            result.returncode = 17

        self.assertEqual(
            [
                call("(43)) my command"),
                call("\t[<failed>]\n"),
                call("(43)) <Command exited with> <17>\n"),
            ],
            AnsiToWin32().stream.write.mock_calls,
        )
        self.assertEqual(
            [
                call(data),
            ],
            stream.write.mock_calls,
        )

    @patch('plix.displays.AnsiToWin32')
    def test_stream_display_py3_with_color(self, AnsiToWin32):
        stream = MagicMock()
        colorizer = GenericColorizer(color_map={
            'error': ('<', '>'),
            'warning': ('(', ')'),
        })
        display = StreamDisplay(stream=stream, colorizer=colorizer)
        display.set_context(commands=["my command"])

        self.assertEqual(AnsiToWin32().stream, display.stream)
        self.assertEqual(stream.buffer, display.binary_stream)

        with display.command(42, "my command") as result:
            data = "DATA".encode('utf-8')
            display.command_output(42, data)
            result.returncode = 17

        self.assertEqual(
            [
                call("(43)) my command"),
                call("\t[<failed>]\n"),
                call("(43)) <Command exited with> <17>\n"),
            ],
            AnsiToWin32().stream.write.mock_calls,
        )
        stream.buffer.write.assert_called_once_with(data)
