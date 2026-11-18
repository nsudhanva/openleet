"""Count Positions on Street With Required Brightness: street length, lamps, requirements."""


def check(n: int, lights: list[list[int]], requirement: list[int]) -> None:
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= len(lights) <= 10**5, "1 <= lights.length <= 10^5"
    assert all(len(x) == 2 for x in lights), "lights[i].length == 2"
    assert all(0 <= p < n for p, _ in lights), "0 <= positioni < n"
    assert all(0 <= r <= 10**5 for _, r in lights), "0 <= rangei <= 10^5"
    assert len(requirement) == n, "requirement.length == n"
    assert all(0 <= v <= 10**5 for v in requirement), "0 <= requirement[i] <= 10^5"
