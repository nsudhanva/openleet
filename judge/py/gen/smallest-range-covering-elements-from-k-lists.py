"""Smallest Range Covering K Lists with k = 3500 sorted lists of 50 values each (175,000
values), random or in disjoint bands so the window must sweep everything."""

from _shapes import pick_shape

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    k = 3500
    nums = []
    for i in range(k):
        if shape == 0:
            lst = sorted(rng.randint(-(10**5), 10**5) for _ in range(50))
        elif shape == 1:
            lo = -(10**5) + i * 57
            lst = sorted(rng.randint(lo, lo + 56) for _ in range(50))
        else:
            lst = sorted(rng.randint(-10, 10) for _ in range(rng.randint(1, 50)))
        nums.append(lst)
    return {"nums": nums}
