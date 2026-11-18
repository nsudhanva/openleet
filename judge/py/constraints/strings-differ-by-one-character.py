"""Strings Differ by One Character: unique equal-length lowercase strings."""


def check(dict: list[str]) -> None:
    assert isinstance(dict, list), "dict is a list"
    assert all(isinstance(s, str) for s in dict), "dict[i] is a string"
    assert sum(len(s) for s in dict) <= 10**5, "number of characters in dict <= 10^5"
    assert len({len(s) for s in dict}) <= 1, "dict[i].length == dict[j].length"
    assert all("a" <= c <= "z" for s in dict for c in s), (
        "dict[i] contains only lowercase English letters"
    )
    assert len(set(dict)) == len(dict), "dict[i] should be unique"
