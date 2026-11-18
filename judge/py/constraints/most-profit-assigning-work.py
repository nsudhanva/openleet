"""Most Profit Assigning Work: job difficulties and profits, and worker abilities."""


def check(difficulty: list[int], profit: list[int], worker: list[int]) -> None:
    assert len(difficulty) == len(profit), "n == difficulty.length == profit.length"
    assert 1 <= len(difficulty) <= 10**4, "1 <= n <= 10^4"
    assert 1 <= len(worker) <= 10**4, "1 <= m <= 10^4"
    for arr in (difficulty, profit, worker):
        assert all(1 <= v <= 10**5 for v in arr), "1 <= difficulty[i], profit[i], worker[i] <= 10^5"
