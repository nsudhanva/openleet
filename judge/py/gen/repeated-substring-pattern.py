"""Strings of length 10^4: a long block repeated (true) or a near-periodic string broken at the
last character (false), so every candidate period must be checked to the end."""

SEEDS = 3
N = 10**4


def generate(rng):
    shape = rng.getrandbits(6) % 3
    if shape == 0:
        # Long period: 5000 repeated twice.
        block = "".join(rng.choice("ab") for _ in range(N // 2))
        return {"s": block * 2}
    if shape == 1:
        # Short period almost everywhere, but the last character breaks it.
        period = rng.choice([1, 2, 4, 5, 8, 10])
        block = "".join(rng.choice("ab") for _ in range(period))
        s = list(block * (N // period))
        s[-1] = "c"
        return {"s": "".join(s)}
    # Prime-ish length with an all-equal prefix: false but every check runs long.
    n = N - 1
    s = "a" * (n - 1) + "b"
    return {"s": s}
