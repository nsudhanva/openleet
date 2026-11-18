"""Count the Number of Computer Unlocking Permutations: an integer array of complexities."""


def check(complexity: list[int]) -> None:
    assert 2 <= len(complexity) <= 10**5, "2 <= complexity.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in complexity), "1 <= complexity[i] <= 10^9"
