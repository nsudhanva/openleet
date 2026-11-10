"""Number of Sets of K Segments at n = 1000 with k near n / 2, the worst case for the
O(n^2 * k) DP."""

SEEDS = 2


def generate(rng):
    n = rng.randint(990, 1000)
    return {"n": n, "k": rng.randint(n // 3, 2 * n // 3)}
