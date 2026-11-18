"""Group Shifted Strings: an array of lowercase strings."""


def check(strings: list[str]) -> None:
    assert 1 <= len(strings) <= 200, "1 <= strings.length <= 200"
    assert all(1 <= len(s) <= 50 for s in strings), "1 <= strings[i].length <= 50"
    assert all("a" <= c <= "z" for s in strings for c in s), (
        "strings[i] consists of lowercase English letters"
    )
