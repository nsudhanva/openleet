"""Path Crossing: a string of N, S, E, W moves."""


def check(path: str) -> None:
    assert isinstance(path, str), "path is a string"
    assert 1 <= len(path) <= 10**4, "1 <= path.length <= 10^4"
    assert all(c in "NSEW" for c in path), "path[i] is either 'N', 'S', 'E', or 'W'"
