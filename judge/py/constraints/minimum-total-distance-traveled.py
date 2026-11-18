"""Minimum Total Distance Traveled: robot positions and factories as [position, limit]."""


def check(robot: list[int], factory: list[list[int]]) -> None:
    assert 1 <= len(robot) <= 100, "1 <= robot.length <= 100"
    assert 1 <= len(factory) <= 100, "1 <= factory.length <= 100"
    assert all(len(f) == 2 for f in factory), "factory[j].length == 2"
    assert all(-(10**9) <= r <= 10**9 for r in robot), "-10^9 <= robot[i] <= 10^9"
    assert all(-(10**9) <= p <= 10**9 for p, _ in factory), "-10^9 <= positionj <= 10^9"
    assert all(0 <= lim <= len(robot) for _, lim in factory), "0 <= limitj <= robot.length"
    assert len(set(robot)) == len(robot), "robot positions are unique"
    assert len({p for p, _ in factory}) == len(factory), "factory positions are unique"
    assert sum(lim for _, lim in factory) >= len(robot), "it is possible to repair every robot"
