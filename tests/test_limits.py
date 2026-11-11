import unittest

from openleet.judging.limits import set_limit


class LimitsTests(unittest.TestCase):
    def test_slow_trusted_reference_is_excluded_only_from_limit_setting(self):
        entry = {"cpuMs": {"dataset": 12, "doocs1": 15, "doocs2": 400, "mercury1": 1}}

        failed = set_limit(entry, None)

        self.assertEqual(failed, [])
        self.assertEqual(entry["cpuMs"], {"dataset": 12, "doocs1": 15})
        self.assertEqual(entry["limitMs"], 1000)

    def test_measured_limits_filter_outliers_after_verdicts(self):
        entry = {}
        measured = {
            "dataset": {"cpuMs": 10, "verdict": "accepted"},
            "doocs1": {"cpuMs": 111, "verdict": "accepted"},
            "doocs2": {"cpuMs": 900, "verdict": "memory_limit_exceeded"},
            "mercury1": {"cpuMs": 1, "verdict": "accepted"},
        }

        failed = set_limit(entry, measured)

        self.assertEqual(failed, ["doocs2"])
        self.assertEqual(entry["cpuMs"], {"dataset": 10})
