"""
Test the configuration parser.
"""

from __future__ import print_function

from unittest import TestCase
from contextlib import contextmanager
from voluptuous import (
    MultipleInvalid,
)
from six import StringIO

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
        loaded_conf = plix.configuration.load_from_stream(stream=stream)
        self.assertEqual(
            ['alpha', 'beta'],
            loaded_conf['script'],
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

        with patch('plix.configuration.open', mocked_open, create=True):
            loaded_conf = plix.configuration.load_from_file(filename='foo.yml')

        self.assertEqual(
            ['alpha', 'beta'],
            loaded_conf['script'],
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
        ref_conf = conf.copy()
        norm_conf = plix.configuration.normalize(conf)

        for key in ref_conf:
            self.assertEqual(ref_conf[key], norm_conf[key])

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
            'script': ['alpha'],
        }

        norm_conf = plix.configuration.normalize(conf)

        self.assertEqual(ref_conf['script'], norm_conf['script'])

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
        ):
            norm_conf = plix.configuration.normalize(conf)

        self.assertEqual(ref_conf['executor'], norm_conf['executor'])

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
        ):
            norm_conf = plix.configuration.normalize(conf)

        self.assertEqual(ref_conf['executor'], norm_conf['executor'])
        my_module.MyExecutor.assert_called_once_with(
            options={
                'a': 'alpha',
                'b': 'beta',
            },
        )
