"""Reorder Data in Log Files: space-separated logs of an identifier plus words."""


def check(logs: list[str]) -> None:
    assert isinstance(logs, list), "logs is a list"
    assert 1 <= len(logs) <= 100, "1 <= logs.length <= 100"
    assert all(isinstance(g, str) for g in logs), "logs[i] is a string"
    assert all(3 <= len(g) <= 100 for g in logs), "3 <= logs[i].length <= 100"
    for g in logs:
        tokens = g.split(" ")
        assert all(tokens), "tokens separated by a single space"
        assert len(tokens) >= 2, "an identifier and at least one word after it"
        words = tokens[1:]
        assert all(w.isascii() and w.islower() and w.isalpha() for w in words) or all(
            w.isascii() and w.isdigit() for w in words
        ), "words are all lowercase letters or all digits"
