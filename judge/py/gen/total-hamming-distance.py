"""Total Hamming Distance at n = 10^4 with values up to 10^9, where the pairwise O(n^2 * 30)
scan is far too slow."""

SEEDS = 2
N = 10**4


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(0, 10**9) for _ in range(N)]
    else:
        nums = [rng.choice([0, 10**9, 2**29 - 1, rng.randint(0, 10**9)]) for _ in range(N)]
    return {"nums": nums}
