"""
Test the main script.
"""

import argparse

from unittest import TestCase

from mock import patch

from plix.main import PairsParser


class MainTests(TestCase):
    @patch(
        'plix.main.load_from_file',
        return_value={},
    )
    def test_parse_args_no_arguments(self, load_from_file_mock):
        from plix.main import parse_args

        args = parse_args([])
        self.assertFalse(args.debug)
        self.assertEqual(load_from_file_mock.return_value, args.configuration)

    @patch(
        'plix.main.load_from_file',
        side_effect=IOError("No such file"),
    )
    def test_parse_args_non_existing_file(self, _):
        from plix.main import parse_args

        with self.assertRaises(SystemExit) as ex:
            parse_args(['-c', 'foo.yml'])

        self.assertEqual(1, ex.exception.code)

    def test_parse_args_pairs(self):
        parser = PairsParser(option_strings=[], dest='pairs')
        args = argparse.Namespace()
        parser(parser=None, namespace=args, values=['a:1'])

        self.assertEqual(
            frozenset({('a', '1')}),
            args.pairs,
        )

    def test_parse_args_invalid_pairs(self):
        parser = PairsParser(option_strings=[], dest='pairs')
        args = argparse.Namespace()

        with self.assertRaises(ValueError):
            parser(parser=None, namespace=args, values=['a;1'])

    @patch(
        'plix.main.load_from_file',
        return_value={},
    )
    def test_main_in_debug_mode(self, _):
        from plix.main import main

        with patch('sys.argv', ['plix', '-d']):
            main()
