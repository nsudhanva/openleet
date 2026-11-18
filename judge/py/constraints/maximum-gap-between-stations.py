"""Maximum Gap Between Stations: a skill string and a longer station string, both lowercase."""


def check(skill: str, station: str) -> None:
    n, m = len(skill), len(station)
    assert 1 <= n <= m <= 10**5, "1 <= n <= m <= 10^5"
    assert all("a" <= c <= "z" for c in skill), "skill consists of lowercase English letters"
    assert all("a" <= c <= "z" for c in station), "station consists of lowercase English letters"
    i = 0
    for c in station:
        if i < n and skill[i] == c:
            i += 1
    assert i == n, "a valid assignment exists for every worker"
