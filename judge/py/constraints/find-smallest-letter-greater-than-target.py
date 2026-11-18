"""Find Smallest Letter Greater Than Target: sorted lowercase letters and a lowercase target."""

from itertools import pairwise


def check(letters: list[str], target: str) -> None:
    assert 2 <= len(letters) <= 10**4, "2 <= letters.length <= 10^4"
    assert all(isinstance(c, str) and len(c) == 1 and "a" <= c <= "z" for c in letters), (
        "letters[i] is a lowercase English letter"
    )
    assert all(a <= b for a, b in pairwise(letters)), "letters is sorted in non-decreasing order"
    assert letters[0] != letters[-1], "letters contains at least two different characters"
    assert isinstance(target, str) and len(target) == 1 and "a" <= target <= "z", (
        "target is a lowercase English letter"
    )
