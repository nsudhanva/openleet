"""Finding the Users Active Minutes: [user ID, minute] action logs and the answer size k."""


def check(logs: list[list[int]], k: int) -> None:
    assert 1 <= len(logs) <= 10**4, "1 <= logs.length <= 10^4"
    assert all(len(r) == 2 for r in logs), "logs[i] == [IDi, timei]"
    assert all(0 <= r[0] <= 10**9 for r in logs), "0 <= IDi <= 10^9"
    assert all(1 <= r[1] <= 10**5 for r in logs), "1 <= timei <= 10^5"
    minutes: dict[int, set[int]] = {}
    for uid, t in logs:
        minutes.setdefault(uid, set()).add(t)
    most = max(len(s) for s in minutes.values())
    assert most <= k <= 10**5, "k is in the range [the maximum UAM for a user, 10^5]"
