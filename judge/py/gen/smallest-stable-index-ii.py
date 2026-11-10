"""Smallest Stable Index II at n = 10^5: decreasing (no index stable, every quadratic scan
runs fully), nearly sorted with the answer at the end, or random."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.getrandbits(6) % 3
    if shape == 0:
        nums = sorted((rng.randint(0, 10**9) for _ in range(N)), reverse=True)
        k = rng.randint(0, 1000)
    elif shape == 1:
        nums = sorted(rng.randint(0, 10**9) for _ in range(N))
        nums[0] = 10**9
        k = rng.randint(0, 10**4)
    else:
        nums = [rng.randint(0, 10**9) for _ in range(N)]
        k = rng.randint(0, 10**9)
    return {"nums": nums, "k": k}
