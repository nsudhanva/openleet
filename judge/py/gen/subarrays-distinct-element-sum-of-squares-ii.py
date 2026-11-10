"""Distinct Element Sum of Squares II at n = 10^5: all distinct (the maximum answer) or
values from a small pool, punishing the quadratic subarray scan."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        nums = rng.sample(range(1, N + 1), N)
    elif shape == 1:
        nums = [rng.randint(1, 50) for _ in range(N)]
    else:
        nums = [rng.randint(1, N) for _ in range(N)]
    return {"nums": nums}
