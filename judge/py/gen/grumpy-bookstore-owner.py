"""Grumpy Bookstore Owner at the maximum n = 2 * 10^4 with a window of about n / 2 minutes, so
summing each window afresh costs ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    customers = [rng.randint(0, 1000) for _ in range(N)]
    grumpy = [rng.randint(0, 1) for _ in range(N)]
    minutes = rng.randint(N * 2 // 5, N * 3 // 5)
    return {"customers": customers, "grumpy": grumpy, "minutes": minutes}
