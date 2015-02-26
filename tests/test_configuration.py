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

from mock import patch

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
        self.assertEqual({'script': ['alpha', 'beta']}, loaded_conf)

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
        ):
            loaded_conf = plix.configuration.load_from_file(filename='foo.yml')

        self.assertEqual({'script': ['alpha', 'beta']}, loaded_conf)

    def test_normalize_with_appropriate_configuration(self):
        conf = {
            'matrix': {
                'alpha': 1,
                'beta': 2,
            },
            'install': ('install.sh',),
            'script': ['alpha'],
        }
        norm_conf = plix.configuration.normalize(conf)
        self.assertEqual(conf, norm_conf)

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
        self.assertEqual(ref_conf, norm_conf)
