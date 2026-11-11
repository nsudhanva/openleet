"""Find Beautiful Indices I at s.length = 10^5: a block of b-matches, a block of a-matches, then
another block of b-matches, with k ~ n/15, so testing each a-match against the b-matches (even from
either end with an early stop) is ~10^9 comparisons."""

SEEDS = 2
N = 10**5


def generate(rng):
    x, y = rng.sample("abcdefghijklmnopqrstuvwxyz", 2)
    l1 = rng.randint(N // 4, N // 3)
    l2 = rng.randint(N // 3, 2 * N // 5)
    a, b = x * rng.randint(1, 3), y * rng.randint(1, 3)
    k = rng.randint(max(1, N // 20), max(1, N // 10))
    return {"s": y * l1 + x * l2 + y * (N - l1 - l2), "a": a, "b": b, "k": k}
