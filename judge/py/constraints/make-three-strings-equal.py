"""Make Three Strings Equal: three lowercase strings."""


def check(s1: str, s2: str, s3: str) -> None:
    for s in (s1, s2, s3):
        assert 1 <= len(s) <= 100, "1 <= length <= 100"
        assert all("a" <= c <= "z" for c in s), "lowercase English letters only"
