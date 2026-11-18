"""String Compression: a list of single characters."""


def check(chars: list[str]) -> None:
    assert isinstance(chars, list), "chars is a list"
    assert 1 <= len(chars) <= 2000, "1 <= chars.length <= 2000"
    assert all(isinstance(c, str) and len(c) == 1 for c in chars), "chars[i] is one character"
