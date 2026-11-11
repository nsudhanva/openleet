"""Minimum Penalty for a Shop at length 10^5 (the limit), so recounting the 'N's before and the
'Y's after every closing hour is quadratic (even with str.count) against one prefix pass."""

SEEDS = 2
N = 10**5


def generate(rng):
    return {"customers": "".join(rng.choice("YN") for _ in range(N))}
