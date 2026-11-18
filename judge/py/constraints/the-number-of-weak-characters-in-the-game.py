"""The Number of Weak Characters in the Game: [attack, defense] per character."""


def check(properties: list[list[int]]) -> None:
    assert 2 <= len(properties) <= 10**5, "2 <= properties.length <= 10^5"
    assert all(len(p) == 2 for p in properties), "properties[i].length == 2"
    assert all(1 <= a <= 10**5 and 1 <= d <= 10**5 for a, d in properties), (
        "1 <= attacki, defensei <= 10^5"
    )
