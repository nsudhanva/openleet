"""Wiggle Subsequence at the maximum n = 1000 with long flat runs and monotone stretches, so
equal neighbours and plateaus must be handled."""

SEEDS = 3
N = 1000


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        nums = [rng.randint(0, 1000) for _ in range(N)]
    elif shape == 1:
        nums = []
        while len(nums) < N:
            nums.extend([rng.randint(0, 1000)] * rng.randint(1, 20))
        nums = nums[:N]
    else:
        nums = sorted(rng.randint(0, 1000) for _ in range(N))
    return {"nums": nums}
