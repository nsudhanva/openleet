"""Subarrays with K Different Integers at n = 2 * 10^4: small pools with a matching k (many
valid windows) or a large k, punishing the quadratic scan."""

SEEDS = 3
N = 2 * 10**4


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        pool = rng.randint(2, 10)
        nums = [rng.randint(1, pool) for _ in range(N)]
        k = rng.randint(1, pool)
    elif shape == 1:
        nums = [rng.randint(1, 2000) for _ in range(N)]
        k = rng.randint(500, 1500)
    else:
        nums = [rng.randint(1, N) for _ in range(N)]
        k = rng.randint(1, 50)
    return {"nums": nums, "k": k}
