"""Contiguous Array at n = 10^5: random bits, or long runs of one value so balanced
subarrays are rare and long."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(0, 1) for _ in range(N)]
    else:
        nums = []
        while len(nums) < N:
            nums += [rng.randint(0, 1)] * rng.randint(1, 5000)
        nums = nums[:N]
    return {"nums": nums}
