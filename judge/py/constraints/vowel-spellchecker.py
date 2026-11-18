"""Vowel Spellchecker: a word list and a list of query words, all English letters."""


def check(wordlist: list[str], queries: list[str]) -> None:
    assert 1 <= len(wordlist) <= 5000, "1 <= wordlist.length <= 5000"
    assert 1 <= len(queries) <= 5000, "1 <= queries.length <= 5000"
    assert all(1 <= len(w) <= 7 for w in wordlist), "1 <= wordlist[i].length <= 7"
    assert all(1 <= len(q) <= 7 for q in queries), "1 <= queries[i].length <= 7"
    assert all(w.isascii() and w.isalpha() for w in [*wordlist, *queries]), (
        "wordlist[i] and queries[i] consist only of English letters"
    )
