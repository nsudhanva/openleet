"""Shifting Letters at n = 10^5 with shifts up to 10^9 (prefix sums overflow 32 bits), so the
quadratic per-prefix approach does 5 * 10^9 work."""

SEEDS = 2


def generate(rng):
    all_max = rng.random() < 0.5
    n = 10**5
    s = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n))
    shifts = [10**9] * n if all_max else [rng.randint(0, 10**9) for _ in range(n)]
    return {"s": s, "shifts": shifts}
