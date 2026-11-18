"""Minimum Amount of Time to Collect Garbage: houses' garbage strings and travel times."""


def check(garbage: list[str], travel: list[int]) -> None:
    assert 2 <= len(garbage) <= 10**5, "2 <= garbage.length <= 10^5"
    assert all(isinstance(g, str) for g in garbage), "garbage[i] is a string"
    assert all(set(g) <= set("MPG") for g in garbage), "garbage[i] consists of only 'M', 'P', 'G'"
    assert all(1 <= len(g) <= 10 for g in garbage), "1 <= garbage[i].length <= 10"
    assert len(travel) == len(garbage) - 1, "travel.length == garbage.length - 1"
    assert all(1 <= t <= 100 for t in travel), "1 <= travel[i] <= 100"
