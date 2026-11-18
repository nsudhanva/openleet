"""Maximum Capacity Within Budget: machine costs, capacities and a budget."""


def check(costs: list[int], capacity: list[int], budget: int) -> None:
    n = len(costs)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert n == len(capacity), "costs.length == capacity.length"
    assert all(1 <= v <= 10**5 for v in costs), "1 <= costs[i] <= 10^5"
    assert all(1 <= v <= 10**5 for v in capacity), "1 <= capacity[i] <= 10^5"
    assert 1 <= budget <= 2 * 10**5, "1 <= budget <= 2 * 10^5"
