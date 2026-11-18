"""Count Beautiful Numbers: an inclusive range [l, r]."""


def check(l: int, r: int) -> None:  # noqa: E741
    assert isinstance(l, int) and isinstance(r, int), "l and r are integers"
    assert 1 <= l <= r < 10**9, "1 <= l <= r < 10^9"
