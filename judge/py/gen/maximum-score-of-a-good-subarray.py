"""Maximum Score of a Good Subarray at n = 3 * 10^4: a mountain of distinct values peaking at k
near the middle, so every step outward sets a new minimum and trying every (i, j) around k, or
rescanning one side per new minimum, costs ~2 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4
TOP = 2 * 10**4


def generate(rng):
    k = N // 2 + rng.randint(-N // 10, N // 10)
    left = sorted(rng.sample(range(1, TOP), k))
    right = sorted(rng.sample(range(1, TOP), N - k - 1), reverse=True)
    return {"nums": [*left, TOP, *right], "k": k}
