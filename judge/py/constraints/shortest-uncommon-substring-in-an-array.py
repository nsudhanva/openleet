"""Shortest Uncommon Substring in an Array: 2 to 100 short lowercase strings."""


def check(arr: list[str]) -> None:
    assert 2 <= len(arr) <= 100, "2 <= n <= 100"
    assert all(1 <= len(s) <= 20 for s in arr), "1 <= arr[i].length <= 20"
    assert all("a" <= ch <= "z" for s in arr for ch in s), (
        "arr[i] consists only of lowercase English letters"
    )
