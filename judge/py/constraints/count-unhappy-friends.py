"""Count Unhappy Friends: n people, their preference lists and the pairing."""


def check(n: int, preferences: list[list[int]], pairs: list[list[int]]) -> None:
    assert isinstance(preferences, list) and isinstance(pairs, list), "preferences, pairs are lists"
    assert 2 <= n <= 500, "2 <= n <= 500"
    assert n % 2 == 0, "n is even"
    assert len(preferences) == n, "preferences.length == n"
    assert all(isinstance(p, list) and len(p) == n - 1 for p in preferences), (
        "preferences[i].length == n - 1"
    )
    assert all(0 <= v <= n - 1 for p in preferences for v in p), "0 <= preferences[i][j] <= n - 1"
    assert all(i not in p for i, p in enumerate(preferences)), "preferences[i] does not contain i"
    assert all(len(set(p)) == len(p) for p in preferences), (
        "all values in preferences[i] are unique"
    )
    assert len(pairs) == n // 2, "pairs.length == n/2"
    assert all(isinstance(p, list) and len(p) == 2 for p in pairs), "pairs[i].length == 2"
    assert all(x != y for x, y in pairs), "xi != yi"
    assert all(0 <= v <= n - 1 for p in pairs for v in p), "0 <= xi, yi <= n - 1"
    people = sorted(v for p in pairs for v in p)
    assert people == list(range(n)), "each person is contained in exactly one pair"
