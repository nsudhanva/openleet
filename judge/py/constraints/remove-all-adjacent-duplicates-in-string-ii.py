"""Remove All Adjacent Duplicates in String II: a lowercase string and a group size k."""


def check(s: str, k: int) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert 2 <= k <= 10**4, "2 <= k <= 10^4"
    assert all("a" <= c <= "z" for c in s), "s only contains lowercase English letters"
