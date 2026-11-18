"""Maximum Performance of a Team: n engineers with speed and efficiency, team size k."""


def check(n: int, speed: list[int], efficiency: list[int], k: int) -> None:
    assert 1 <= k <= n <= 10**5, "1 <= k <= n <= 10^5"
    assert len(speed) == n, "speed.length == n"
    assert len(efficiency) == n, "efficiency.length == n"
    assert all(1 <= v <= 10**5 for v in speed), "1 <= speed[i] <= 10^5"
    assert all(1 <= v <= 10**8 for v in efficiency), "1 <= efficiency[i] <= 10^8"
