"""Stable Subarrays With Equal Boundary and Interior Sum: an integer array."""


def check(capacity: list[int]) -> None:
    assert 3 <= len(capacity) <= 10**5, "3 <= capacity.length <= 10^5"
    assert all(-(10**9) <= v <= 10**9 for v in capacity), "-10^9 <= capacity[i] <= 10^9"
