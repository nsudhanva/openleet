"""Number of Employees Who Met the Target: hours worked and a target."""


def check(hours: list[int], target: int) -> None:
    assert 1 <= len(hours) <= 50, "1 <= n == hours.length <= 50"
    assert all(0 <= h <= 10**5 for h in hours), "0 <= hours[i] <= 10^5"
    assert 0 <= target <= 10**5, "0 <= target <= 10^5"
