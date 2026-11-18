"""Merge Similar Items: two lists of [value, weight] pairs with unique values."""


def check(items1: list[list[int]], items2: list[list[int]]) -> None:
    for items in (items1, items2):
        assert 1 <= len(items) <= 1000, "1 <= items.length <= 1000"
        assert all(len(i) == 2 for i in items), "items[i].length == 2"
        assert all(1 <= v <= 1000 for i in items for v in i), "1 <= valuei, weighti <= 1000"
        assert len({i[0] for i in items}) == len(items), "each valuei is unique"
