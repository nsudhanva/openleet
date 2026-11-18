"""Delete Columns to Make Sorted: n lowercase strings of the same length."""


def check(strs: list[str]) -> None:
    n = len(strs)
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(isinstance(s, str) for s in strs), "strs[i] is a string"
    assert all(1 <= len(s) <= 1000 for s in strs), "1 <= strs[i].length <= 1000"
    assert all(len(s) == len(strs[0]) for s in strs), "all strings have the same length"
    assert all("a" <= c <= "z" for s in strs for c in s), (
        "strs[i] consists of lowercase English letters"
    )
