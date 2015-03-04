"""
Test the configuration parser.
"""

from __future__ import print_function

import sys

from unittest import TestCase
from contextlib import contextmanager
from voluptuous import (
    MultipleInvalid,
)

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

from mock import (
    patch,
    MagicMock,
)

import plix.configuration


class ConfigurationTests(TestCase):
    def test_load_from_stream(self):
        stream = StringIO(
            u"""
            script:
              - alpha
              - beta
            """,
        )
        with patch(
            'plix.configuration.ShellExecutor',
            return_value=None,
        ):
            loaded_conf = plix.configuration.load_from_stream(stream=stream)
        self.assertEqual(
            {
                'executor': None,
                'script': ['alpha', 'beta'],
            },
            loaded_conf,
        )

    def test_load_from_file(self):
        @contextmanager
        def mocked_open(*args, **kwargs):
            yield StringIO(
                u"""
                script:
                - alpha
                - beta
                """,
            )

        with patch(
                'builtins.open'
                if sys.version_info >= (3, 0)
                else '__builtin__.open',
                mocked_open,
                create=True,
        ), patch(
            'plix.configuration.ShellExecutor',
            return_value=None,
        ):
            loaded_conf = plix.configuration.load_from_file(filename='foo.yml')

        self.assertEqual(
            {
                'executor': None,
                'script': ['alpha', 'beta'],
            },
            loaded_conf,
        )

    def test_command_or_command_list_with_strings(self):
        value = "hello"
        self.assertEqual(
            [value],
            plix.configuration.command_or_command_list(value),
        )

    def test_command_or_command_list_with_lists(self):
        value = ["hello"]
        self.assertEqual(
            value,
            plix.configuration.command_or_command_list(value),
        )

    def test_command_or_command_list_with_tuples(self):
        value = ("hello",)
        self.assertEqual(
            value,
            plix.configuration.command_or_command_list(value),
        )

    def test_command_or_command_list_with_int(self):
        with self.assertRaises(ValueError):
            plix.configuration.command_or_command_list(42)

    def test_command_or_command_list_with_floats(self):
        with self.assertRaises(ValueError):
            plix.configuration.command_or_command_list(42.0)

    def test_command_or_command_list_with_none(self):
        with self.assertRaises(ValueError):
            plix.configuration.command_or_command_list(None)

    def test_normalize_with_appropriate_configuration(self):
        conf = {
            'matrix': {
                'alpha': 1,
                'beta': 2,
            },
            'install': ('install.sh',),
            'script': ['alpha'],
        }

        with patch(
            'plix.configuration.ShellExecutor',
            return_value=None,
        ):
            norm_conf = plix.configuration.normalize(conf)

        ref_conf = conf.copy()
        ref_conf.update(executor=None)
        self.assertEqual(ref_conf, norm_conf)

    def test_normalize_with_inappropriate_configuration(self):
        conf = {
            'matrix': [],
            'script': {
                'key': 'value',
            },
        }

        with self.assertRaises(MultipleInvalid) as ex:
            plix.configuration.normalize(conf)

        self.assertEqual(2, len(ex.exception.errors))

    def test_normalize_transforms_values(self):
        conf = {
            'script': 'alpha',
        }
        ref_conf = {
            'executor': None,
            'script': ['alpha'],
        }

        with patch(
            'plix.configuration.ShellExecutor',
            return_value=None,
        ):
            norm_conf = plix.configuration.normalize(conf)

        self.assertEqual(ref_conf, norm_conf)

    def test_normalize_parses_executors(self):
        my_module = MagicMock()
        my_executor = my_module.MyExecutor()

        conf = {
            'executor': 'my_module.MyExecutor',
        }
        ref_conf = {
            'executor': my_executor,
        }

        with patch.dict(
            'sys.modules',
            {'my_module': my_module},
        ), patch(
            'plix.configuration.ShellExecutor',
            return_value=None,
        ):
            norm_conf = plix.configuration.normalize(conf)

        self.assertEqual(ref_conf, norm_conf)

    def test_normalize_parses_executors_with_options(self):
        my_module = MagicMock()
        my_executor = my_module.MyExecutor()
        my_module.MyExecutor.reset_mock()

        conf = {
            'executor': {
                'name': 'my_module.MyExecutor',
                'options': {
                    'a': 'alpha',
                    'b': 'beta',
                },
            },
        }
        ref_conf = {
            'executor': my_executor,
        }

        with patch.dict(
            'sys.modules',
            {'my_module': my_module},
        ), patch(
            'plix.configuration.ShellExecutor',
            return_value=None,
        ):
            norm_conf = plix.configuration.normalize(conf)

        self.assertEqual(ref_conf, norm_conf)
        my_module.MyExecutor.assert_called_once_with(
            options={
                'a': 'alpha',
                'b': 'beta',
            },
        )
