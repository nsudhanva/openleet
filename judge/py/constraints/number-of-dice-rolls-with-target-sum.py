"""Number of Dice Rolls With Target Sum: dice count, faces and a target."""


def check(n: int, k: int, target: int) -> None:
    assert 1 <= n <= 30, "1 <= n <= 30"
    assert 1 <= k <= 30, "1 <= k <= 30"
    assert 1 <= target <= 1000, "1 <= target <= 1000"
