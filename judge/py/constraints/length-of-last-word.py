"""Length of Last Word: a string of English letters and spaces."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**4, "1 <= s.length <= 10^4"
    assert all(c == " " or (c.isascii() and c.isalpha()) for c in s), (
        "s consists of only English letters and spaces"
    )
    assert s.strip(" ") != "", "there is at least one word in s"
