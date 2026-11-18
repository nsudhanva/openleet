"""Tag Validator: a string of code made of letters, digits and a few symbols."""


def check(code: str) -> None:
    assert isinstance(code, str), "code is a string"
    assert 1 <= len(code) <= 500, "1 <= code.length <= 500"
    allowed = set("<>/![]. ")
    assert all(c.isascii() and (c.isalnum() or c in allowed) for c in code), (
        "code consists of English letters, digits, '<', '>', '/', '!', '[', ']', '.', and ' '"
    )
