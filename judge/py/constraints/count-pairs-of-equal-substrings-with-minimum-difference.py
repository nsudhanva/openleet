"""Count Pairs of Equal Substrings With Minimum Difference: two lowercase strings."""


def _lower(s: str) -> bool:
    return all("a" <= c <= "z" for c in s)


def check(firstString: str, secondString: str) -> None:
    assert isinstance(firstString, str) and isinstance(secondString, str), "strings"
    assert 1 <= len(firstString) <= 2 * 10**5, "1 <= firstString.length <= 2 * 10^5"
    assert 1 <= len(secondString) <= 2 * 10**5, "1 <= secondString.length <= 2 * 10^5"
    assert _lower(firstString), "firstString has only lowercase English letters"
    assert _lower(secondString), "secondString has only lowercase English letters"
