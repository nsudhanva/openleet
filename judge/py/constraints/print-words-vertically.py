"""Print Words Vertically: a sentence of upper case words separated by single spaces."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 200, "1 <= s.length <= 200"
    assert all(c == " " or "A" <= c <= "Z" for c in s), (
        "s contains only upper case English letters (and spaces)"
    )
    assert "  " not in s.strip(" "), "only one space between 2 words"
