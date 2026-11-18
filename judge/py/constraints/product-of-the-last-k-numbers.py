"""Product of the Last K Numbers: a stream of add and getProduct calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert isinstance(ops, list) and isinstance(args, list), "ops and args are arrays"
    assert len(ops) == len(args) and ops, "one argument list per operation"
    assert ops[0] == "ProductOfNumbers" and args[0] == [], "ProductOfNumbers() takes no arguments"
    assert len(ops) - 1 <= 4 * 10**4, "at most 4 * 10^4 calls to add and getProduct"
    count = 0
    # Entries that are not 1 as (position, value); ones never change a product.
    significant: list[tuple[int, int]] = []
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert isinstance(a, list) and len(a) == 1, "each call takes one argument"
        if op == "add":
            assert isinstance(a[0], int) and 0 <= a[0] <= 100, "0 <= num <= 100"
            if a[0] != 1:
                significant.append((count, a[0]))
            count += 1
        else:
            assert op == "getProduct", "operations are add and getProduct"
            k = a[0]
            assert isinstance(k, int) and 1 <= k <= 4 * 10**4, "1 <= k <= 4 * 10^4"
            assert k <= count, "the current list has at least k numbers"
            product = 1
            for pos, v in reversed(significant):
                if pos < count - k or v == 0:
                    break
                product *= v
                assert product < 2**31, "the product fits in a 32-bit integer"
