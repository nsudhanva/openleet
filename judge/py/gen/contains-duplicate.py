"""Contains Duplicate at n = 10^5: all distinct (a full pass), or the only duplicate pair at
the very end."""

SEEDS = 2
N = 10**5


def generate(rng):
    nums = rng.sample(range(-(10**9), 10**9 + 1), N)
    if rng.random() < 0.5:
        nums[-1] = nums[-2]
    return {"nums": nums}
