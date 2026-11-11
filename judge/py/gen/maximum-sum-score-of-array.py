"""Maximum Sum Score of Array at n = 5 * 10^4, so summing the prefix and suffix afresh at every
index costs ~2.5 * 10^9 additions."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    return {"nums": [rng.randint(-(10**5), 10**5) for _ in range(N)]}
