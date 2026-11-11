"""Longest Special Path II on a 10^4-node tree that is mostly one long path of distinct values, so
walking down from every node costs ~5 * 10^7 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    # Node i hangs off one of the last few nodes; a few values repeat so the path splits.
    edges = []
    for v in range(1, N):
        u = max(0, v - 1 - int(rng.expovariate(1.0)))
        edges.append([u, v, rng.randint(1, 1000)])
    rng.shuffle(edges)
    nums = rng.sample(range(5 * 10**4 + 1), N)
    for _ in range(rng.randint(3, 8)):
        nums[rng.randrange(N)] = nums[rng.randrange(N)]
    return {"edges": edges, "nums": nums}
