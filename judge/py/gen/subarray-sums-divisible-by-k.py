"""Subarray Sums Divisible by K at n = 3 * 10^4 with negative values (the negative-modulo
trap) and multiples of k, punishing the quadratic scan."""

SEEDS = 3
N = 3 * 10**4


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    k = rng.randint(2, 10**4)
    if shape == 0:
        nums = [rng.randint(-(10**4 // k), 10**4 // k) * k for _ in range(N)]
    elif shape == 1:
        k = rng.randint(2, 10)
        nums = [rng.randint(-(10**4), 10**4) for _ in range(N)]
    else:
        nums = [rng.randint(-(10**4), 10**4) for _ in range(N)]
    return {"nums": nums, "k": k}
