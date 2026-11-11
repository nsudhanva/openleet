"""Minimum Sum of Values by Dividing Array at n = 10^4 and m = 10: ten blocks, each of supersets
of its andValue, so trying every split point for every segment end is ~5 * 10^8 steps."""

SEEDS = 2
N = 10**4
M = 10


def generate(rng):
    cuts = sorted(rng.sample(range(1, N), M - 1))
    bounds = [0, *cuts, N]
    nums, and_values = [], []
    for j in range(M):
        v = rng.randrange(1, 1 << 16) & rng.randrange(1 << 16)
        and_values.append(v)
        length = bounds[j + 1] - bounds[j]
        block = [v | rng.randrange(1, 1 << 16) for _ in range(length)]
        block[rng.randrange(length)] = v or 1
        nums += block
    return {"nums": nums, "andValues": and_values}
