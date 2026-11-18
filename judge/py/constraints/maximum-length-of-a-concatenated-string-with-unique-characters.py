"""Maximum Length of a Concatenated String with Unique Characters: up to 16 lowercase strings."""


def check(arr: list[str]) -> None:
    assert 1 <= len(arr) <= 16, "1 <= arr.length <= 16"
    for s in arr:
        assert isinstance(s, str), "arr[i] is a string"
        assert 1 <= len(s) <= 26, "1 <= arr[i].length <= 26"
        assert all("a" <= c <= "z" for c in s), "arr[i] contains only lowercase English letters"
