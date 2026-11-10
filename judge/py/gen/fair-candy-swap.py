"""Fair Candy Swap with 10^4 boxes each and exactly one valid swap (values are multiples of 7
apart from three planted boxes whose residues rule out every other pair), so the answer is
unique and a quadratic pair scan does ~10^8 checks."""

SEEDS = 2
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
    n = rng.choice([10**4, rng.randint(5000, 10**4)])
    m = rng.choice([10**4, rng.randint(5000, 10**4)])
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
    alice = [*a_rest, x, w1, w2]
    bob = [*b_rest, y]
    rng.shuffle(alice)
    rng.shuffle(bob)
    return {"aliceSizes": alice, "bobSizes": bob}
