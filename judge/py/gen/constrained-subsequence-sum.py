"""Constrained Subsequence Sum at n = 5 * 10^4 with k between n / 4 and n / 2 (mostly negative or
evenly mixed values), or at n = 10^5 with k near 10^4 where the best sums climb to a peak and then
fall by 1 per step, so the window's maximum is always its oldest entry: ~10^9 steps either way to
take each window's maximum afresh."""

from _shapes import pick_shape

SEEDS = 3
N = 5 * 10**4
LONG = 10**5
TOP = 10**4


def staircase(rng):
    k = rng.randint(TOP * 9 // 10, TOP)
    climb = LONG // TOP + rng.randint(1, 4)
    nums = [TOP] * climb
    nums += [-(j + 1) for j in range(k)]
    nums += [-k] * (LONG - len(nums))
    return {"nums": nums[:LONG], "k": k}


def generate(rng):
    shape = pick_shape(rng)
    if shape == 2:
        return staircase(rng)
    low = -(10**4) if shape == 0 else -500
    nums = [
        rng.randint(low, 10**4) if rng.random() < 0.5 else rng.randint(-(10**4), -1)
        for _ in range(N)
    ]
    return {"nums": nums, "k": rng.randint(N // 4, N // 2)}
