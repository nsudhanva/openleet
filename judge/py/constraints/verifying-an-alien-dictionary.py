"""Verifying an Alien Dictionary: lowercase words and a 26-letter order string."""


def check(words: list[str], order: str) -> None:
    assert 1 <= len(words) <= 100, "1 <= words.length <= 100"
    assert all(1 <= len(w) <= 20 for w in words), "1 <= words[i].length <= 20"
    assert len(order) == 26, "order.length == 26"
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words), (
        "all characters in words[i] are English lowercase letters"
    )
    assert order.isascii() and order.isalpha() and order.islower(), (
        "all characters in order are English lowercase letters"
    )
    assert len(set(order)) == 26, "order is a permutation of the lowercase letters"
