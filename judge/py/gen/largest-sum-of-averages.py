"""Largest Sum of Averages at n = 100 with k around n / 2, where trying every partition is
exponential."""

SEEDS = 2
N = 100


def generate(rng):
    nums = [rng.randint(1, 10**4) for _ in range(N)]
    return {"nums": nums, "k": rng.randint(N // 3, 2 * N // 3)}
