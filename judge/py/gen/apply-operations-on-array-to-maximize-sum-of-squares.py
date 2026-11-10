"""Maximize Sum of Squares at n = 10^5 with values up to 10^9 and k from 1 to n, so per-pair
simulation is far too slow and the answer needs the modulus."""

SEEDS = 3
N = 10**5


def generate(rng):
    nums = [rng.randint(1, 10**9) for _ in range(N)]
    k = rng.choice([1, rng.randint(1, N), N])
    return {"nums": nums, "k": k}
