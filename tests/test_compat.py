# coding=utf-8

"""
Tests for the Python 2/Python 3 compatibility layer.
"""

from __future__ import unicode_literals

from unittest import TestCase

from plix.compat import yaml_dump


class CompatTest(TestCase):
    def test_yaml_dump(self):
        value = {
            "key": "value",
            "animal": ["éléphant"],
        }
        self.assertEqual(
            "animal: [éléphant]\nkey: value\n",
            yaml_dump(value),
        )
