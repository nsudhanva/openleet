"""Pyramid Transition Matrix: a bottom row and a list of allowed triples over A to F."""


def check(bottom: str, allowed: list[str]) -> None:
    letters = set("ABCDEF")
    assert isinstance(bottom, str) and isinstance(allowed, list), (
        "bottom is a string, allowed an array"
    )
    assert 2 <= len(bottom) <= 6, "2 <= bottom.length <= 6"
    assert 0 <= len(allowed) <= 216, "0 <= allowed.length <= 216"
    assert all(isinstance(a, str) and len(a) == 3 for a in allowed), "allowed[i].length == 3"
    assert set(bottom) <= letters, "letters are from {'A', 'B', 'C', 'D', 'E', 'F'}"
    assert all(set(a) <= letters for a in allowed), (
        "letters are from {'A', 'B', 'C', 'D', 'E', 'F'}"
    )
    assert len(set(allowed)) == len(allowed), "all values of allowed are unique"
