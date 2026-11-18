"""Analyze User Website Visit Pattern: parallel arrays of username, timestamp, website."""

from collections import Counter


def check(username: list[str], timestamp: list[int], website: list[str]) -> None:
    n = len(username)
    assert 3 <= n <= 50, "3 <= username.length <= 50"
    assert len(timestamp) == n, "timestamp.length == username.length"
    assert len(website) == n, "website.length == username.length"
    assert all(1 <= len(u) <= 10 for u in username), "1 <= username[i].length <= 10"
    assert all(1 <= len(w) <= 10 for w in website), "1 <= website[i].length <= 10"
    assert all(1 <= t <= 10**9 for t in timestamp), "1 <= timestamp[i] <= 10^9"
    assert all(all("a" <= c <= "z" for c in s) for s in username + website), (
        "username[i] and website[i] consist of lowercase English letters"
    )
    assert max(Counter(username).values()) >= 3, "at least one user visited at least three websites"
    assert len(set(zip(username, timestamp, website, strict=True))) == n, (
        "All the tuples are unique"
    )
