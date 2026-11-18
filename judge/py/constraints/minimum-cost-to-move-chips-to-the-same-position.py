"""Minimum Cost to Move Chips to the Same Position: chip positions."""


def check(position: list[int]) -> None:
    assert 1 <= len(position) <= 100, "1 <= position.length <= 100"
    assert all(1 <= x <= 10**9 for x in position), "1 <= position[i] <= 10^9"
