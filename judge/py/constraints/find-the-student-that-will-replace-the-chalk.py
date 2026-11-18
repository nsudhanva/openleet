"""Find the Student that Will Replace the Chalk: chalk usage per student and k pieces."""


def check(chalk: list[int], k: int) -> None:
    assert 1 <= len(chalk) <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= v <= 10**5 for v in chalk), "1 <= chalk[i] <= 10^5"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
