"""Unique Word Abbreviation: ValidWordAbbr(dictionary) then isUnique(word) calls."""


def _word(w: object, name: str) -> None:
    assert isinstance(w, str), f"{name} is a string"
    assert 1 <= len(w) <= 20, f"1 <= {name}.length <= 20"
    assert all("a" <= c <= "z" for c in w), f"{name} consists of lowercase English letters"


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert ops[0] == "ValidWordAbbr", "first operation is the constructor"
    assert len(args[0]) == 1 and isinstance(args[0][0], list), "constructor takes dictionary"
    dictionary = args[0][0]
    assert 1 <= len(dictionary) <= 3 * 10**4, "1 <= dictionary.length <= 3 * 10^4"
    for w in dictionary:
        _word(w, "dictionary[i]")
    assert all(op == "isUnique" for op in ops[1:]), "only isUnique is called after construction"
    assert len(ops) - 1 <= 5000, "at most 5000 calls to isUnique"
    for a in args[1:]:
        assert len(a) == 1, "isUnique takes one argument"
        _word(a[0], "word")
