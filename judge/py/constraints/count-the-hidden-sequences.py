"""Count the Hidden Sequences: differences with lower and upper bounds."""


def check(differences: list[int], lower: int, upper: int) -> None:
    assert 1 <= len(differences) <= 10**5, "1 <= n <= 10^5"
    assert all(-(10**5) <= d <= 10**5 for d in differences), "-10^5 <= differences[i] <= 10^5"
    assert -(10**5) <= lower <= upper <= 10**5, "-10^5 <= lower <= upper <= 10^5"
