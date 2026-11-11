"""Count Ways to Group Overlapping Ranges with 4 * 10^4 ranges in ~50 clusters of mutually
overlapping ranges, so a pairwise scan, or a sweep that joins each range with every open one, costs
~2 * 10^7 to 8 * 10^8 steps."""

SEEDS = 2
N = 4 * 10**4
TOP = 10**9
LO, HI = 400, 1200  # cluster sizes


def generate(rng):
    sizes, left = [], N
    while left > 0:
        sizes.append(min(left, rng.randint(LO, HI)))
        left -= sizes[-1]
    # One cluster per slot of the line; every range in a cluster covers its centre.
    slot = TOP // len(sizes)
    ranges = []
    for c, size in enumerate(sizes):
        centre = c * slot + slot // 2
        reach = slot // 2 - 1
        for _ in range(size):
            ranges.append([centre - rng.randint(0, reach), centre + rng.randint(0, reach)])
    rng.shuffle(ranges)
    return {"ranges": ranges}
