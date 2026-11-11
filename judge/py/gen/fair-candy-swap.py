"""Fair Candy Swap with 10^4 boxes each and exactly one valid swap, its two boxes last (values are
multiples of 7 apart from three planted boxes whose residues rule out every other pair), so a
quadratic pair scan does all ~10^8 checks."""

SEEDS = 2
N = 10**4
TOP = 99995  # largest multiple of 7 within 10^5


def adjust(values, delta):
    """Shift multiples of 7 in values (kept in [7, TOP]) toward a sum change of delta; return
    what is left over."""
    for i in range(len(values)):
        if delta == 0:
            break
        step = min(TOP - values[i], delta) if delta > 0 else max(7 - values[i], delta)
        values[i] += step
        delta -= step
    return delta


def generate(rng):
    n = m = N
    y = 7 * rng.randint(1, 14000)
    x = y + 7 * rng.randint(-100, 100) + 1
    x = min(max(x, 1), 99996)
    if (x - y) % 7 != 1:
        x = y + 1
    k = x - y
    w1 = 7 * rng.randint(0, 14000) + 3
    w2 = 7 * rng.randint(0, 14000) + 5
    a_rest = [7 * rng.randint(1, TOP // 7) for _ in range(n - 3)]
    b_rest = [7 * rng.randint(1, TOP // 7) for _ in range(m - 1)]
    diff = (sum(a_rest) + x + w1 + w2) - (sum(b_rest) + y) - 2 * k
    # Raising Bob's total by diff, or lowering Alice's, balances the swap.
    if adjust(a_rest, -adjust(b_rest, diff)):
        raise ValueError("cannot balance")
    # Bob's other boxes must not hold y, or a scan over Bob's boxes would meet it early.
    for i, v in enumerate(b_rest):
        if v == y:
            step = 7 if y + 7 <= TOP else -7
            j = next(
                j for j, u in enumerate(b_rest) if j != i and 7 <= u - step <= TOP and u - step != y
            )
            b_rest[i] += step
            b_rest[j] -= step
    alice = [*a_rest, w1, w2]
    rng.shuffle(alice)
    rng.shuffle(b_rest)
    return {"aliceSizes": [*alice, x], "bobSizes": [*b_rest, y]}
