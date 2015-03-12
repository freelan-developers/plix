"""
Test the main script.
"""

from unittest import TestCase
from argparse import Namespace
from mock import patch

from plix.main import (
    PairsParser,
    parse_args,
    main,
)

from .common import (
    PythonExecutor,
    MockDisplay,
)


class MainTests(TestCase):
    @patch(
        'plix.main.load_from_file',
        return_value={},
    )
    def test_parse_args_no_arguments(self, load_from_file_mock):
        args = parse_args([])
        self.assertFalse(args.debug)
        self.assertEqual(load_from_file_mock.return_value, args.configuration)

    @patch(
        'plix.main.load_from_file',
        side_effect=IOError("No such file"),
    )
    def test_parse_args_non_existing_file(self, _):
        with self.assertRaises(SystemExit) as ex:
            parse_args(['-c', 'foo.yml'])

        self.assertEqual(1, ex.exception.code)

    def test_parse_args_pairs(self):
        parser = PairsParser(option_strings=[], dest='pairs')
        args = Namespace()
        parser(parser=None, namespace=args, values=['a:1'])

        self.assertEqual(
            frozenset({('a', '1')}),
            args.pairs,
        )

    def test_parse_args_invalid_pairs(self):
        parser = PairsParser(option_strings=[], dest='pairs')
        args = Namespace()

        with self.assertRaises(ValueError):
            parser(parser=None, namespace=args, values=['a;1'])

    @patch('plix.main.parse_args')
    def test_main_in_debug_mode(self, parse_args):
        x = []

        parse_args.return_value = Namespace(
            configuration={
                'executor': PythonExecutor(globals=globals(), locals=locals()),
                'script': [
                    'x.append(42)',
                    'x.append(123)',
                ],
            },
            debug=True,
        )

        main(args=['-d'], display=MockDisplay())

        self.assertEqual([42, 123], x)
