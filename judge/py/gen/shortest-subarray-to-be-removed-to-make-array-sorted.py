"""Shortest Subarray to be Removed at n = 4 * 10^4: two sorted halves drawn from the same range, so
pairing each prefix end with a linear scan of the suffix does ~n^2 / 8 steps."""

SEEDS = 2
N = 4 * 10**4
LIMIT = 10**9


def generate(rng):
    half = N // 2
    a = sorted(rng.randint(0, LIMIT) for _ in range(half))
    b = sorted(rng.randint(0, LIMIT) for _ in range(N - half))
    a[-1] = LIMIT
    b[0] = 0
    return {"arr": a + b}
