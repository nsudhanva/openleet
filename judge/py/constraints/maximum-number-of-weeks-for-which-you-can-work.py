"""Maximum Number of Weeks for Which You Can Work: milestones per project."""


def check(milestones: list[int]) -> None:
    assert 1 <= len(milestones) <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= v <= 10**9 for v in milestones), "1 <= milestones[i] <= 10^9"
