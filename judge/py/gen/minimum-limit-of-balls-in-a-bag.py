"""Minimum Limit of Balls in a Bag with 10^5 bags of up to 10^9 balls and up to 10^9
operations; scanning candidate limits one by one is hopeless."""

SEEDS = 3
N = 10**5


def generate(rng):
    nums = [rng.randint(1, 10**9) for _ in range(N)]
    return {"nums": nums, "maxOperations": rng.choice((1, 10**9, rng.randint(1, 10**9)))}
