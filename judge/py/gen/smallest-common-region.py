"""Smallest Common Region over ~10^4 region lists forming two chains of ~5000 below a short trunk
(or one chain), with the two regions deep down, so looking up each parent by scanning every list
is ~10^4 scans of 10^4 lists."""

from _shapes import pick_shape

SEEDS = 3
LISTS = 10**4
TRUNK = 5
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate(rng):
    shape = pick_shape(rng)
    names, seen = [], set()

    def fresh():
        while True:
            w = "".join(rng.choice(LETTERS) for _ in range(rng.randint(6, 20)))
            if w not in seen:
                seen.add(w)
                names.append(w)
                return w

    trunk = [fresh() for _ in range(TRUNK)]
    branches = 1 if shape == 2 else 2
    depth = (LISTS - TRUNK) // branches
    chains = [[fresh() for _ in range(depth)] for _ in range(branches)]
    regions = []
    for i, x in enumerate(trunk):
        kids = [trunk[i + 1]] if i + 1 < TRUNK else [c[0] for c in chains]
        regions.append([x, *kids, *(fresh() for _ in range(rng.randint(0, 2)))])
    bottoms = []
    for chain in chains:
        for i, x in enumerate(chain):
            extra = [fresh() for _ in range(rng.randint(1 if i + 1 == len(chain) else 0, 3))]
            regions.append([x, *chain[i + 1 : i + 2], *extra])
        bottoms.append(regions[-1][-1])
    rng.shuffle(regions)
    region1 = bottoms[0]
    if shape == 0:
        region2 = bottoms[1]
    elif shape == 1:
        region2 = chains[0][rng.randrange(max(1, depth // 10))]
    else:
        region2 = regions[[r[0] for r in regions].index(trunk[0])][-1]
    if rng.random() < 0.5:
        region1, region2 = region2, region1
    return {"regions": regions, "region1": region1, "region2": region2}
