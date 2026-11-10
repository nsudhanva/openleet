"""Single Element in a Sorted Array at n = 99,999 (49,999 pairs plus one single) with the single
at either end or in the middle."""

SEEDS = 3


def generate(rng):
    where = rng.getrandbits(6) % 3
    m = 49999
    values = sorted(rng.sample(range(0, 10**5 + 1), m + 1))
    single = [0, m, rng.randint(0, m)][where]
    nums = []
    for i, v in enumerate(values):
        nums += [v] if i == single else [v, v]
    return {"nums": nums}
