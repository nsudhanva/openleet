"""Rings and Rods: color/rod pairs, such as "B0R6"."""


def check(rings: str) -> None:
    assert isinstance(rings, str), "rings is a string"
    assert len(rings) % 2 == 0, "rings.length == 2 * n"
    assert 1 <= len(rings) // 2 <= 100, "1 <= n <= 100"
    assert all(c in "RGB" for c in rings[0::2]), "rings[i] where i is even is 'R', 'G', or 'B'"
    assert all("0" <= c <= "9" for c in rings[1::2]), (
        "rings[i] where i is odd is a digit from '0' to '9'"
    )
