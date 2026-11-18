"""Most Popular Video Creator: parallel arrays of creators, video ids and view counts."""


def check(creators: list[str], ids: list[str], views: list[int]) -> None:
    n = len(creators)
    assert len(ids) == n and len(views) == n, "n == creators.length == ids.length == views.length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    for s in creators + ids:
        assert 1 <= len(s) <= 5, "1 <= creators[i].length, ids[i].length <= 5"
        assert s.isascii() and s.isalpha() and s.islower(), (
            "creators[i] and ids[i] consist only of lowercase English letters"
        )
    assert all(0 <= v <= 10**5 for v in views), "0 <= views[i] <= 10^5"
