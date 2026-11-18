"""Special Binary String: a balanced 0/1 string whose prefixes never have more 0s than 1s."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 50, "1 <= s.length <= 50"
    assert all(c in "01" for c in s), "s[i] is either '0' or '1'"
    bal = 0
    for c in s:
        bal += 1 if c == "1" else -1
        assert bal >= 0, "every prefix has at least as many 1s as 0s"
    assert bal == 0, "s has equal numbers of 0s and 1s"
