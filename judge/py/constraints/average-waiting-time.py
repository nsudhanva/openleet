"""Average Waiting Time: customers [arrival, time] sorted by arrival."""


def check(customers: list[list[int]]) -> None:
    assert 1 <= len(customers) <= 10**5, "1 <= customers.length <= 10^5"
    assert all(len(c) == 2 for c in customers), "customers[i] = [arrival_i, time_i]"
    assert all(1 <= a <= 10**4 and 1 <= t <= 10**4 for a, t in customers), (
        "1 <= arrival_i, time_i <= 10^4"
    )
    assert all(customers[i][0] <= customers[i + 1][0] for i in range(len(customers) - 1)), (
        "arrival_i <= arrival_i+1"
    )
