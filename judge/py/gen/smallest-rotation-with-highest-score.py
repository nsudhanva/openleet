"""Smallest Rotation with Highest Score at n = 10^5, so checking every rotation in O(n) each
is 10^10 work."""

SEEDS = 3


def generate(rng):
    shape = rng.getrandbits(6) % 3
    n = 10**5
    if shape == 0:
        nums = [rng.randrange(n) for _ in range(n)]
    elif shape == 1:
        nums = list(range(n))
        rng.shuffle(nums)
    else:
        nums = [rng.randrange(5) for _ in range(n)]
    return {"nums": nums}
