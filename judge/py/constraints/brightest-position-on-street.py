"""Brightest Position on Street: lamps as [position, range] pairs."""


def check(lights: list[list[int]]) -> None:
    assert 1 <= len(lights) <= 10**5, "1 <= lights.length <= 10^5"
    assert all(len(lamp) == 2 for lamp in lights), "lights[i].length == 2"
    assert all(-(10**8) <= p <= 10**8 for p, _ in lights), "-10^8 <= positioni <= 10^8"
    assert all(0 <= r <= 10**8 for _, r in lights), "0 <= rangei <= 10^8"
