"""Simplify Path: an absolute Unix path."""


def check(path: str) -> None:
    assert 1 <= len(path) <= 3000, "1 <= path.length <= 3000"
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./_")
    assert set(path) <= allowed, "path consists of English letters, digits, '.', '/' or '_'"
    assert path[0] == "/", "path is a valid absolute Unix path"
