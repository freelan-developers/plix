"""
Test the main script.
"""

from unittest import TestCase

from mock import patch

from plix.main import main
from plix.configuration import Configuration


class MainTests(TestCase):
    def test_main_no_arguments(self):
        configuration = Configuration(conf={})

        with patch(
                'plix.configuration.Configuration.load_from_file',
                return_value=configuration,
        ):
            with patch('sys.argv', ['plix']):
                main()

    def test_main_non_existing_file(self):
        with patch(
                'plix.configuration.Configuration.load_from_file',
                side_effect=IOError("No such file"),
        ):
            with patch('sys.argv', ['plix', '-c', 'foo.yml']):
                with self.assertRaises(SystemExit) as ex:
                    main()

        self.assertEqual(1, ex.exception.code)

    def test_main_in_debug_mode(self):
        configuration = Configuration(conf={})

        with patch(
                'plix.configuration.Configuration.load_from_file',
                return_value=configuration,
        ):
            with patch('sys.argv', ['plix', '-d']):
                main()
