"""One Edit Distance: two alphanumeric strings."""

import re


def check(s: str, t: str) -> None:
    assert isinstance(s, str) and isinstance(t, str), "s and t are strings"
    assert 0 <= len(s) <= 10**4, "0 <= s.length <= 10^4"
    assert 0 <= len(t) <= 10**4, "0 <= t.length <= 10^4"
    assert re.fullmatch(r"[A-Za-z0-9]*", s), "s consists of letters and digits"
    assert re.fullmatch(r"[A-Za-z0-9]*", t), "t consists of letters and digits"
