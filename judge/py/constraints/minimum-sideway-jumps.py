"""Minimum Sideway Jumps: obstacle lane (0..3) at each point of a 3-lane road."""


def check(obstacles: list[int]) -> None:
    n = len(obstacles) - 1
    assert 1 <= n <= 5 * 10**5, "1 <= n <= 5 * 10^5"
    assert all(0 <= v <= 3 for v in obstacles), "0 <= obstacles[i] <= 3"
    assert obstacles[0] == obstacles[n] == 0, "obstacles[0] == obstacles[n] == 0"
