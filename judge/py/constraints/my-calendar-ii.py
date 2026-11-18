"""My Calendar II: a MyCalendarTwo() constructor then book(start, end) calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "one argument list per operation"
    assert ops[0] == "MyCalendarTwo" and args[0] == [], "constructor is MyCalendarTwo()"
    assert all(op == "book" for op in ops[1:]), "only book is called after construction"
    assert len(ops) - 1 <= 1000, "at most 1000 calls will be made to book"
    for a in args[1:]:
        assert len(a) == 2, "book takes startTime and endTime"
        assert 0 <= a[0] < a[1] <= 10**9, "0 <= start < end <= 10^9"
