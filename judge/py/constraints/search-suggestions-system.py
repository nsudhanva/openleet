"""Search Suggestions System: unique lowercase product names plus a lowercase search word."""

import string


def check(products: list[str], searchWord: str) -> None:
    low = set(string.ascii_lowercase)
    assert 1 <= len(products) <= 1000, "1 <= products.length <= 1000"
    assert all(isinstance(p, str) and 1 <= len(p) <= 3000 for p in products), (
        "1 <= products[i].length <= 3000"
    )
    assert 1 <= sum(len(p) for p in products) <= 2 * 10**4, (
        "1 <= sum(products[i].length) <= 2 * 10^4"
    )
    assert len(set(products)) == len(products), "all the strings of products are unique"
    assert all(set(p) <= low for p in products), "products[i] consists of lowercase English letters"
    assert isinstance(searchWord, str) and 1 <= len(searchWord) <= 1000, (
        "1 <= searchWord.length <= 1000"
    )
    assert set(searchWord) <= low, "searchWord consists of lowercase English letters"
