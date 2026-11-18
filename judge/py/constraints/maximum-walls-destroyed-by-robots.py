"""Maximum Walls Destroyed by Robots: robot positions, shot distances and wall positions."""


def check(robots: list[int], distance: list[int], walls: list[int]) -> None:
    assert 1 <= len(robots) <= 10**5, "1 <= robots.length <= 10^5"
    assert len(distance) == len(robots), "robots.length == distance.length"
    assert 1 <= len(walls) <= 10**5, "1 <= walls.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in robots), "1 <= robots[i] <= 10^9"
    assert all(1 <= v <= 10**9 for v in walls), "1 <= walls[j] <= 10^9"
    assert all(1 <= d <= 10**5 for d in distance), "1 <= distance[i] <= 10^5"
    assert len(set(robots)) == len(robots), "all values in robots are unique"
    assert len(set(walls)) == len(walls), "all values in walls are unique"
