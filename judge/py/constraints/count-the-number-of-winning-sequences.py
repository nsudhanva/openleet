"""Count The Number of Winning Sequences: a string over F, W, E."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert set(s) <= {"F", "W", "E"}, "s[i] is one of 'F', 'W', or 'E'"
