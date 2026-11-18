"""Taking Maximum Energy From the Mystic Dungeon: energy values and a jump k."""


def check(energy: list[int], k: int) -> None:
    n = len(energy)
    assert 1 <= n <= 10**5, "1 <= energy.length <= 10^5"
    assert all(-1000 <= e <= 1000 for e in energy), "-1000 <= energy[i] <= 1000"
    assert 1 <= k <= n - 1, "1 <= k <= energy.length - 1"
