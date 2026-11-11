"""Minimum Space Wasted From Packaging with 10^4 packages and 10^4 suppliers of 10 boxes each (the
10^5 box total), every supplier able to fit the largest package, so walking all packages for
each supplier is 10^8 steps against binary searching at each box."""

SEEDS = 2
N = 10**4
M = 10**4
PER = 10
LIMIT = 10**5


def generate(rng):
    packages = [rng.randint(1, LIMIT) for _ in range(N)]
    top = max(packages)
    boxes = []
    for _ in range(M):
        box = rng.sample(range(1, LIMIT + 1), PER)
        if max(box) < top:
            big = rng.randint(top, LIMIT)
            while big in box:
                big = rng.randint(top, LIMIT)
            box[rng.randrange(PER)] = big
        boxes.append(box)
    return {"packages": packages, "boxes": boxes}
