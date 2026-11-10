"""Tests for the harness's input sizes and the calibration work."""

import unittest

import calibrate
import harness

FUNCTION = {"kind": "function"}


class SizeTests(unittest.TestCase):
    def test_lists_strings_and_numbers(self):
        size = harness.size(FUNCTION, {"nums": [3] * 100_000, "s": "ab", "k": 7, "flag": True})
        self.assertEqual(size, "nums: 100,000 items, s: 2 characters, k = 7")

    def test_a_matrix_reads_as_rows_by_columns_and_pairs_as_a_count(self):
        grid = [[0] * 300 for _ in range(200)]
        matrix = "grid: 200 \N{MULTIPLICATION SIGN} 300"
        self.assertEqual(harness.size(FUNCTION, {"grid": grid}), matrix)
        edges = [[1, 2]] * 5
        self.assertEqual(harness.size(FUNCTION, {"edges": edges}), "edges: 5 items")
        words = ["abc", "de"]
        self.assertEqual(harness.size(FUNCTION, {"words": words}), "words: 2 items")

    def test_huge_numbers_are_counted_in_digits(self):
        self.assertEqual(harness.size(FUNCTION, {"n": 10**40}), "n: 41 digits")
        self.assertEqual(harness.size(FUNCTION, {"n": -(10**9)}), "n = -1,000,000,000")

    def test_design_problems_count_calls(self):
        data = {"ops": ["Cache", "put", "get"], "args": [[2], [1, 1], [1]]}
        self.assertEqual(harness.size({"kind": "design"}, data), "2 calls")


class CalibrationTests(unittest.TestCase):
    def test_measures_a_positive_time(self):
        self.assertGreater(calibrate.measure(), 0)


if __name__ == "__main__":
    unittest.main()
