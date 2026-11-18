"""Design Movie Rental System: MovieRentingSystem calls."""


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
    _shape(ops, args, "MovieRentingSystem", 2, {"drop": 2, "rent": 2, "report": 0, "search": 1})
    n, entries = args[0]
    assert isinstance(n, int) and 1 <= n <= 3 * 10**5, "1 <= n <= 3 * 10^5"
    assert isinstance(entries, list) and 1 <= len(entries) <= 10**5, "1 <= entries.length <= 10^5"
    assert all(isinstance(e, list) and len(e) == 3 for e in entries), "entries[i].length == 3"
    assert all(all(isinstance(x, int) for x in e) for e in entries), "integer entries"
    assert all(0 <= e[0] < n for e in entries), "0 <= shopi < n"
    assert all(1 <= e[1] <= 10**4 and 1 <= e[2] <= 10**4 for e in entries), (
        "1 <= moviei, pricei <= 10^4"
    )
    carried = {(e[0], e[1]) for e in entries}
    assert len(carried) == len(entries), "each shop carries at most one copy of a movie"
    assert len(ops) - 1 <= 10**5, "at most 10^5 calls"
    rented = set()
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "rent":
            assert tuple(a) in carried, "rent refers to a shop that carries the movie"
            assert tuple(a) not in rented, "rent only on an unrented copy"
            rented.add(tuple(a))
        elif op == "drop":
            assert tuple(a) in rented, "drop only on a previously rented copy"
            rented.discard(tuple(a))
