"""Simple Bank System: a Bank built from balances, then deposit/transfer/withdraw calls."""

_LIMIT = 10**12


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "Bank" and len(args[0]) == 1, "constructor takes balance"
    balance = args[0][0]
    assert 1 <= len(balance) <= 10**5, "1 <= n <= 10^5"
    assert all(0 <= b <= _LIMIT for b in balance), "0 <= balance[i] <= 10^12"
    arity = {"deposit": 2, "withdraw": 2, "transfer": 3}
    counts = dict.fromkeys(arity, 0)
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in arity, "only deposit, transfer and withdraw are called"
        assert len(a) == arity[op], "argument count matches the function"
        counts[op] += 1
        accounts = a[:-1]
        assert all(1 <= x <= 10**5 for x in accounts), "1 <= account, account1, account2 <= 10^5"
        assert 0 <= a[-1] <= _LIMIT, "0 <= money <= 10^12"
    assert all(c <= 10**4 for c in counts.values()), "at most 10^4 calls to each function"
