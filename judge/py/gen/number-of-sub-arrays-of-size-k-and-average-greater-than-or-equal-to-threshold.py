"""Sub-arrays of Size K at n = 10^5 with a large window, so recomputing each window sum is
quadratic."""

SEEDS = 2
N = 10**5


def generate(rng):
    arr = [rng.randint(1, 10**4) for _ in range(N)]
    k = rng.randint(N // 4, N // 2)
    return {"arr": arr, "k": k, "threshold": rng.randint(4900, 5100)}
