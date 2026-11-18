"""Car Fleet: a target, unique car positions and car speeds."""


def check(target: int, position: list[int], speed: list[int]) -> None:
    assert isinstance(position, list) and isinstance(speed, list), "position, speed are lists"
    n = len(position)
    assert n == len(speed), "n == position.length == speed.length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 0 < target <= 10**6, "0 < target <= 10^6"
    assert all(0 <= p < target for p in position), "0 <= position[i] < target"
    assert len(set(position)) == n, "All the values of position are unique"
    assert all(0 < s <= 10**6 for s in speed), "0 < speed[i] <= 10^6"
