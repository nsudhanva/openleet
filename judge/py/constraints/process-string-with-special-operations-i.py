"""Process String with Special Operations I: a short string of lowercase letters and * # %."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 20, "1 <= s.length <= 20"
    assert all("a" <= c <= "z" or c in "*#%" for c in s), (
        "s consists of only lowercase English letters and *, #, %"
    )
