"""
Test matrices functions.
"""

from unittest import TestCase

import plix.matrix

from plix.exceptions import UnknownKeys


class MatrixTests(TestCase):
    def test_find_required_keys_single_key(self):
        keys = plix.matrix.find_required_keys("Hello {{world}} !")
        self.assertEqual({'world'}, keys)

    def test_find_required_keys_multiple_keys(self):
        keys = plix.matrix.find_required_keys(
            "{{a.x}} * {{b.y}} = {{a.x * b.y}}",
        )
        self.assertEqual({'a', 'b'}, keys)

    def test_find_required_keys_no_keys(self):
        keys = plix.matrix.find_required_keys("Hello world !")
        self.assertEqual(set(), keys)

    def test_find_required_keys_multiple_commands(self):
        keys = plix.matrix.find_required_keys(
            "{{a}}",
            "{{b}}",
            "",
        )
        self.assertEqual({'a', 'b'}, keys)

    def test_generate_variants(self):
        matrix = {
            'a': [1, 2],
            'b': [3, 4],
            'c': [5],
        }
        variants = set(plix.matrix.generate_variants(matrix=matrix))
        self.assertEqual(
            {
                frozenset({('a', 1), ('b', 3), ('c', 5)}),
                frozenset({('a', 2), ('b', 3), ('c', 5)}),
                frozenset({('a', 1), ('b', 4), ('c', 5)}),
                frozenset({('a', 2), ('b', 4), ('c', 5)}),
            },
            variants,
        )

    def test_generate_limited_variants(self):
        matrix = {
            'a': [1, 2],
            'b': [3, 4],
            'c': [5],
        }
        subset_pairs = {('b', 3)}
        variants = set(plix.matrix.generate_variants(
            matrix=matrix,
            subset_pairs=subset_pairs,
        ))
        self.assertEqual(
            {
                frozenset({('a', 1), ('b', 3), ('c', 5)}),
                frozenset({('a', 2), ('b', 3), ('c', 5)}),
            },
            variants,
        )

    def test_validate_keys(self):
        matrix = {
            'a': [1, 2],
            'b': [3, 4],
            'c': [5],
        }
        keys = {'b', 'c'}
        result = plix.matrix.validate_keys(matrix=matrix, keys=keys)
        self.assertEqual(
            {
                'b': [3, 4],
                'c': [5],
            },
            result,
        )

    def test_validate_keys_with_unknown_keys(self):
        matrix = {
            'a': [1, 2],
            'b': [3, 4],
            'c': [5],
        }
        keys = {'b', 'c', 'd'}

        with self.assertRaises(UnknownKeys) as ex:
            plix.matrix.validate_keys(matrix=matrix, keys=keys)

        self.assertEqual(ex.exception.keys, frozenset({'d'}))
