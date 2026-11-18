"""Minimum Cost to Hire K Workers: worker qualities, minimum wages and a group size k."""


def check(quality: list[int], wage: list[int], k: int) -> None:
    n = len(quality)
    assert n == len(wage), "n == quality.length == wage.length"
    assert 1 <= k <= n <= 10**4, "1 <= k <= n <= 10^4"
    assert all(1 <= x <= 10**4 for x in quality), "1 <= quality[i] <= 10^4"
    assert all(1 <= x <= 10**4 for x in wage), "1 <= wage[i] <= 10^4"
