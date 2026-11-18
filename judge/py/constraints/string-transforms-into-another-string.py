"""String Transforms Into Another String: two equal-length lowercase strings."""


def check(str1: str, str2: str) -> None:
    assert isinstance(str1, str) and isinstance(str2, str), "str1 and str2 are strings"
    assert 1 <= len(str1) <= 10**4, "1 <= str1.length <= 10^4"
    assert len(str1) == len(str2), "str1.length == str2.length"
    for s in (str1, str2):
        assert all("a" <= c <= "z" for c in s), (
            "str1 and str2 contain only lowercase English letters"
        )
