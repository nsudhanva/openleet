"""Process String with Special Operations II: a string of lowercase letters and * # % and an
index k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("a" <= c <= "z" or c in "*#%" for c in s), (
        "s consists of only lowercase English letters and *, #, %"
    )
    assert 0 <= k <= 10**15, "0 <= k <= 10^15"
    length = 0
    limit = 10**15 + len(s)
    for c in s:
        if c == "#":
            length *= 2
        elif c == "*":
            length = max(0, length - 1)
        elif c != "%":
            length += 1
        assert length <= limit, "the length of result after processing s will not exceed 10^15"
    assert length <= 10**15, "the length of result after processing s will not exceed 10^15"
