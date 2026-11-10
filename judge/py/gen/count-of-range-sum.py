"""Count of Range Sum at n = 10^5: huge random values (few matching ranges), or a slow random
walk of small values with a narrow window; both keep the answer far below 2^31."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(-(2**31), 2**31 - 1) for _ in range(N)]
        lower = rng.randint(-(10**5), 10**5)
        upper = rng.randint(lower, 10**5)
    else:
        nums = [rng.randint(-10, 10) for _ in range(N)]
        lower = rng.randint(-5, 0)
        upper = rng.randint(0, 5)
    return {"nums": nums, "lower": lower, "upper": upper}
