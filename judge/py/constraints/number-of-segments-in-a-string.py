"""Number of Segments in a String: a short string whose only space is ' '."""

_ALLOWED = set("!@#$%^&*()_+-=',.:")


def check(s: str) -> None:
    assert 0 <= len(s) <= 300, "0 <= s.length <= 300"
    assert all(c == " " or (c.isascii() and c.isalnum()) or c in _ALLOWED for c in s), (
        "s consists of letters, digits, ' ' or one of !@#$%^&*()_+-=',.:"
    )
