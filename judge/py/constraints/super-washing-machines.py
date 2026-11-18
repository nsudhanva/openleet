"""Super Washing Machines: dresses in each machine."""


def check(machines: list[int]) -> None:
    assert 1 <= len(machines) <= 10000, "1 <= machines.length <= 10000"
    assert all(0 <= v <= 100000 for v in machines), "0 <= machines[i] <= 10^5"
