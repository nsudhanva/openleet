"""Largest Subarray Length K at the maximum n = 10^5 with k about n / 2, so comparing every
window as its own slice copies ~2.5 * 10^9 elements even at C speed."""

SEEDS = 2
N = 10**5


def generate(rng):
    nums = rng.sample(range(1, 10**6), N)
    return {"nums": nums, "k": rng.randint(N * 2 // 5, N * 3 // 5)}
