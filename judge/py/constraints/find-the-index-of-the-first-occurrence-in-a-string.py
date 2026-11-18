"""Find the Index of the First Occurrence in a String: a haystack and a needle."""


def check(haystack: str, needle: str) -> None:
    assert isinstance(haystack, str) and isinstance(needle, str), "haystack and needle are strings"
    assert 1 <= len(haystack) <= 10**4, "1 <= haystack.length <= 10^4"
    assert 1 <= len(needle) <= 10**4, "1 <= needle.length <= 10^4"
    assert all("a" <= c <= "z" for c in haystack + needle), (
        "haystack and needle consist of only lowercase English characters"
    )
