"""Design Add and Search Words Data Structure: WordDictionary calls."""


def _shape(ops, args, ctor, ctor_arity, sig):
    assert isinstance(ops, list) and isinstance(args, list), "ops and args are lists"
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert ops[0] == ctor, "first operation is the constructor"
    assert all(isinstance(a, list) for a in args), "each args[i] is a list"
    assert len(args[0]) == ctor_arity, "constructor argument count"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in sig, "known method name"
        assert len(a) == sig[op], "argument count of " + op


def check(ops: list[str], args: list[list]) -> None:
    _shape(ops, args, "WordDictionary", 0, {"addWord": 1, "search": 1})
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls"
    for op, a in zip(ops[1:], args[1:], strict=True):
        w = a[0]
        assert isinstance(w, str) and 1 <= len(w) <= 25, "1 <= word.length <= 25"
        if op == "addWord":
            assert all("a" <= c <= "z" for c in w), "word in addWord is lowercase English letters"
        else:
            assert all(c == "." or "a" <= c <= "z" for c in w), (
                "word in search is '.' or lowercase letters"
            )
            assert w.count(".") <= 2, "at most 2 dots in word for search"
