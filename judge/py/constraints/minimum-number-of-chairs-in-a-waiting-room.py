"""Minimum Number of Chairs in a Waiting Room: a string of entries 'E' and exits 'L'."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 50, "1 <= s.length <= 50"
    assert all(c in "EL" for c in s), "s consists only of the letters 'E' and 'L'"
    inside = 0
    for c in s:
        inside += 1 if c == "E" else -1
        assert inside >= 0, "s represents a valid sequence of entries and exits"
