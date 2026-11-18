"""Naming a Company: a list of distinct lowercase idea names."""


def check(ideas: list[str]) -> None:
    assert 2 <= len(ideas) <= 5 * 10**4, "2 <= ideas.length <= 5 * 10^4"
    assert all(isinstance(s, str) and 1 <= len(s) <= 10 for s in ideas), (
        "1 <= ideas[i].length <= 10"
    )
    assert all(s.isascii() and s.isalpha() and s.islower() for s in ideas), (
        "ideas[i] consists of lowercase English letters"
    )
    assert len(set(ideas)) == len(ideas), "all the strings in ideas are unique"
