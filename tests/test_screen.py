import tempfile
import unittest
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from openleet.judging import TESTS_PATH
from openleet.judging.screen import CONSTRAINTS_DIR, by_slug, loaded, rejected, violation


def module(source: str):
    directory = tempfile.mkdtemp()
    path = Path(directory) / "sample.py"
    path.write_text(source)
    return loaded(path, f"constraints_test_{abs(hash(source))}")


def stored_rejected(item: tuple[str, list[tuple[int, str, str]]]) -> tuple[str, list]:
    """The stored (not generated) tests of a problem its constraints reject."""
    slug, tests = item
    return slug, rejected(slug, [t for t in tests if t[1] != "stress"])


class ScreenTest(unittest.TestCase):
    def test_violation_names_the_failed_constraint(self) -> None:
        check = module(
            "def check(nums):\n"
            "    assert 1 <= len(nums) <= 3, '1 <= nums.length <= 3'\n"
            "    assert nums[0] >= 0, 'nums[i] >= 0'\n"
        )
        assert violation(check, {"nums": [1, 2]}) is None
        assert violation(check, {"nums": []}) == ("1 <= nums.length <= 3", False)
        assert violation(check, {"nums": [-1]}) == ("nums[i] >= 0", False)

    def test_a_check_that_raises_is_flagged_as_its_own_failure(self) -> None:
        check = module("def check(nums):\n    nums[5]\n")
        reason, error = violation(check, {"nums": [1]}) or ("", False)
        assert error
        assert reason.startswith("IndexError")

    @unittest.skipUnless(TESTS_PATH.exists(), "no corpus (uv run openleet judge fetch)")
    def test_every_stored_test_keeps_its_problems_constraints(self) -> None:
        """The corpus holds no test its problem's constraints reject (`judge screen` drops
        them), and every statement example passes its problem's constraints."""
        slugs = sorted(p.stem for p in CONSTRAINTS_DIR.glob("*.py"))
        with ProcessPoolExecutor() as pool:
            found = dict(pool.map(stored_rejected, by_slug(slugs).items(), chunksize=8))
        broken = {
            slug: [(r.idx, r.kind, r.reason) for r in bad[:3]] for slug, bad in found.items() if bad
        }
        assert not broken, broken


if __name__ == "__main__":
    unittest.main()
