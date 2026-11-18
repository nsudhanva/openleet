"""Reformat Phone Number: a string of digits, spaces and dashes."""


def check(number: str) -> None:
    assert 2 <= len(number) <= 100, "2 <= number.length <= 100"
    assert all(c.isascii() and (c.isdigit() or c in "- ") for c in number), (
        "number consists of digits and the characters '-' and ' '"
    )
    assert sum(c.isdigit() for c in number) >= 2, "there are at least two digits in number"
