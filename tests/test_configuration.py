"""
Test the configuration parser.
"""

from __future__ import print_function

import sys
from unittest import TestCase
from contextlib import contextmanager

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

from mock import patch

from plix.configuration import Configuration


class ConfigurationTests(TestCase):
    def test_load_from_stream(self):
        stream = StringIO(
            u"""
            script:
              - alpha
              - beta
            """,
        )
        configuration = Configuration.load_from_stream(stream=stream)
        self.assertEqual({'script': ['alpha', 'beta']}, configuration.conf)

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
            configuration = Configuration.load_from_file(filename='foo.yml')

        self.assertEqual({'script': ['alpha', 'beta']}, configuration.conf)

    def test_configuration_init(self):
        conf = {
            'script': [
                'alpha',
                'beta',
            ],
        }
        configuration = Configuration(conf=conf)
        self.assertEqual(conf, configuration.conf)
