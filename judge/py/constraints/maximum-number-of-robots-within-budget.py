"""Maximum Number of Robots Within Budget: charge times, running costs and a budget."""


def check(chargeTimes: list[int], runningCosts: list[int], budget: int) -> None:
    assert len(chargeTimes) == len(runningCosts), "chargeTimes.length == runningCosts.length"
    assert 1 <= len(chargeTimes) <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert all(1 <= v <= 10**5 for v in chargeTimes), "1 <= chargeTimes[i] <= 10^5"
    assert all(1 <= v <= 10**5 for v in runningCosts), "1 <= runningCosts[i] <= 10^5"
    assert 1 <= budget <= 10**15, "1 <= budget <= 10^15"
