"""Construct Uniform Parity Array II at n = 10^5 distinct values up to 10^9: random parities,
or all even but one odd value placed at the end."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        nums = rng.sample(range(1, 10**9 + 1), N)
    elif shape == 1:
        nums = [2 * v for v in rng.sample(range(1, 5 * 10**8 + 1), N - 1)]
        nums.append(2 * rng.randint(0, 5 * 10**8 - 1) + 1)
    else:
        nums = [2 * v + 1 for v in rng.sample(range(5 * 10**8), N - 1)]
        nums.append(2 * rng.randint(1, 5 * 10**8))
    return {"nums1": nums}
