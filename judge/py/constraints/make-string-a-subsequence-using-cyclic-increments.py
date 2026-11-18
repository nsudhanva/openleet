"""Make String a Subsequence Using Cyclic Increments: two lowercase strings."""


def check(str1: str, str2: str) -> None:
    assert 1 <= len(str1) <= 10**5, "1 <= str1.length <= 10^5"
    assert 1 <= len(str2) <= 10**5, "1 <= str2.length <= 10^5"
    for s in (str1, str2):
        assert all("a" <= c <= "z" for c in s), "lowercase English letters only"
