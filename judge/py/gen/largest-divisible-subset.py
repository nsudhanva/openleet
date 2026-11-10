"""Largest Divisible Subset with 1000 distinct values up to 2 * 10^9: all 31 powers of two
(the unique longest possible chain) hidden among random odd fillers."""

SEEDS = 2
N = 1000
LIMIT = 2 * 10**9


def generate(rng):
    chain = [1 << i for i in range(31)]
    used = set(chain)
    nums = list(chain)
    while len(nums) < N:
        v = rng.randrange(3, LIMIT, 2)
        if v not in used:
            used.add(v)
            nums.append(v)
    rng.shuffle(nums)
    return {"nums": nums}
