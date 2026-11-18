"""Number Of Ways To Reconstruct A Tree: a list of unique [x, y] pairs with x < y."""


def check(pairs: list[list[int]]) -> None:
    assert 1 <= len(pairs) <= 10**5, "1 <= pairs.length <= 10^5"
    assert all(len(p) == 2 for p in pairs), "pairs[i].length == 2"
    assert all(1 <= x < y <= 500 for x, y in pairs), "1 <= xi < yi <= 500"
    assert len({(x, y) for x, y in pairs}) == len(pairs), "the elements in pairs are unique"
