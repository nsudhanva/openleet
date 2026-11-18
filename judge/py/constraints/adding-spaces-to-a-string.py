"""Adding Spaces to a String: a letter string and increasing insertion indices."""

from itertools import pairwise


def check(s: str, spaces: list[int]) -> None:
    assert 1 <= len(s) <= 3 * 10**5, "1 <= s.length <= 3 * 10^5"
    assert s.isascii() and s.isalpha(), "s consists only of lowercase and uppercase English letters"
    assert 1 <= len(spaces) <= 3 * 10**5, "1 <= spaces.length <= 3 * 10^5"
    assert all(0 <= p <= len(s) - 1 for p in spaces), "0 <= spaces[i] <= s.length - 1"
    assert all(a < b for a, b in pairwise(spaces)), (
        "All the values of spaces are strictly increasing"
    )
