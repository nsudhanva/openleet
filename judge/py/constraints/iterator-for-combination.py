"""Iterator for Combination: a constructor then next and hasNext calls."""

from math import comb


def check(ops: list[str], args: list[list]) -> None:
    assert isinstance(ops, list) and isinstance(args, list), "ops and args are lists"
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "CombinationIterator", "first operation is the constructor"
    assert all(o in ("next", "hasNext") for o in ops[1:]), (
        "only next and hasNext follow the constructor"
    )
    assert len(args[0]) == 2, "constructor takes (characters, combinationLength)"
    chars, length = args[0]
    assert isinstance(chars, str) and isinstance(length, int), (
        "characters is a string, length an int"
    )
    assert 1 <= length <= len(chars) <= 15, "1 <= combinationLength <= characters.length <= 15"
    assert all("a" <= c <= "z" for c in chars), "characters are lowercase English letters"
    assert all(chars[i] < chars[i + 1] for i in range(len(chars) - 1)), (
        "characters are sorted and unique"
    )
    assert all(a == [] for a in args[1:]), "next and hasNext take no arguments"
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls to next and hasNext"
    remaining = comb(len(chars), length)
    for o in ops[1:]:
        if o == "next":
            assert remaining > 0, "all calls of next are valid"
            remaining -= 1
