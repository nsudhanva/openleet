"""Rank Teams by Votes: equal-length rankings of uppercase team letters."""


def check(votes: list[str]) -> None:
    assert 1 <= len(votes) <= 1000, "1 <= votes.length <= 1000"
    k = len(votes[0])
    assert 1 <= k <= 26, "1 <= votes[i].length <= 26"
    assert all(len(v) == k for v in votes), "votes[i].length == votes[j].length"
    assert all(c.isascii() and c.isupper() for v in votes for c in v), (
        "votes[i][j] is an English uppercase letter"
    )
    assert all(len(set(v)) == len(v) for v in votes), "all characters of votes[i] are unique"
    first = set(votes[0])
    assert all(first <= set(v) for v in votes), "characters of votes[0] occur in every votes[j]"
