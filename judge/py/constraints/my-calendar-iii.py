"""My Calendar III: a MyCalendarThree constructor followed by book(start, end) calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "MyCalendarThree" and args[0] == [], "constructor takes no arguments"
    assert all(op == "book" for op in ops[1:]), "only book is called"
    assert len(ops) - 1 <= 400, "at most 400 calls will be made to book"
    for a in args[1:]:
        assert len(a) == 2, "book(start, end)"
        assert 0 <= a[0] < a[1] <= 10**9, "0 <= startTime < endTime <= 10^9"
