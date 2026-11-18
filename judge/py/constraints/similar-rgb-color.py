"""Similar RGB Color: a '#' followed by six hex digits."""


def check(color: str) -> None:
    assert len(color) == 7, "color.length == 7"
    assert color[0] == "#", "color[0] == '#'"
    assert all(c in "0123456789abcdef" for c in color[1:]), (
        "color[i] is a digit or 'a'..'f' for i > 0"
    )
