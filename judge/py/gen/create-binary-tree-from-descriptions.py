"""Create Binary Tree From Descriptions with 10^4 shuffled edges and unique values up to
10^5: a random tree, or a single chain 10^4 deep."""

SEEDS = 2
E = 10**4


def generate(rng):
    vals = rng.sample(range(1, 10**5 + 1), E + 1)
    descriptions = []
    if rng.random() < 0.5:
        for i in range(1, E + 1):
            descriptions.append([vals[i - 1], vals[i], rng.randint(0, 1)])
    else:
        slots = [(0, 0), (0, 1)]
        for i in range(1, E + 1):
            j = rng.randrange(len(slots))
            slots[j], slots[-1] = slots[-1], slots[j]
            p, side = slots.pop()
            descriptions.append([vals[p], vals[i], 1 - side])
            slots += [(i, 0), (i, 1)]
    rng.shuffle(descriptions)
    return {"descriptions": descriptions}
