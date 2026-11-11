"""Grumpy Bookstore Owner at the maximum n = 2 * 10^4 with a window of about n / 2 minutes, over
four seeds, so summing each window afresh, even with C-speed slice sums, costs ~4 * 10^8 element
additions in total."""

SEEDS = 4
N = 2 * 10**4


def generate(rng):
    customers = [rng.randint(0, 1000) for _ in range(N)]
    grumpy = [rng.randint(0, 1) for _ in range(N)]
    minutes = rng.randint(N * 9 // 20, N * 11 // 20)
    return {"customers": customers, "grumpy": grumpy, "minutes": minutes}
