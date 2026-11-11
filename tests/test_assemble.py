import unittest
from unittest.mock import patch

from openleet.judging import assemble


class AssembleTests(unittest.TestCase):
    def test_unordered_float_matching_sorts_structurally(self):
        unordered = assemble.matcher("unordered", True)
        nested = assemble.matcher("unordered_nested", True)

        self.assertTrue(unordered([2.0, 10.00001], [2.00001, 9.99999]))
        self.assertTrue(
            nested(
                [[10.00001, 2], [4.000001, 3]],
                [[3, 4.000002], [2.00001, 9.99999]],
            )
        )
        normalized = assemble.normalize([10, 2.0, 2], "unordered")
        self.assertEqual([type(value) for value in normalized], [float, int, int])

    def test_a_reference_memory_failure_drops_only_that_test(self):
        item = {
            "slug": "memory-case",
            "examples": [{"input": {"n": 1}, "output": 1}],
            "inputs": [{"n": 2}, {"n": 3}, {"n": 4}],
            "spec": {"kind": "function", "returns": "int"},
            "starter": "",
            "anyOrder": False,
            "voters": {"dataset": "trusted", "doocs1": "trusted", "mercury1": "crowd"},
        }
        votes = {
            "dataset": {
                "results": [{"out": 1}, {"out": 2}, {"error": "MLE"}, {"out": 4}],
                "cpuMs": 50,
            },
            "doocs1": {
                "results": [{"out": 1}, {"out": 2}, {"out": 3}, {"out": 4}],
                "cpuMs": 55,
            },
            "mercury1": {
                "results": [{"out": 1}, {"out": 2}, {"out": 3}, {"out": 4}],
                "cpuMs": 60,
            },
        }

        with patch.object(assemble, "stress_tests", return_value=([], {})):
            entry, tests = assemble.judge_problem(item, votes)

        self.assertEqual(entry["voters"], ["dataset", "doocs1", "mercury1"])
        self.assertEqual(
            [test["test"].get("input") for test in tests], [{"n": 1}, {"n": 2}, {"n": 4}]
        )
