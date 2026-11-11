"""Find Closest Node to Given Two Nodes at n = 3 * 10^4: node1 and node2 head long tails that
join a long path or a long cycle, so walking from both nodes again for every candidate node is
~10^9 steps."""

from itertools import pairwise

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    order = list(range(N))
    rng.shuffle(order)
    edges = [-1] * N
    # order = tail1 + tail2 + core; each tail runs into the core at its own entry point.
    t1, t2 = rng.randint(N // 5, N // 3), rng.randint(N // 5, N // 3)
    tail1, tail2, core = order[:t1], order[t1 : t1 + t2], order[t1 + t2 :]
    for path in (tail1, tail2, core):
        for u, v in pairwise(path):
            edges[u] = v
    cycle = rng.random() < 0.5
    if cycle:
        edges[core[-1]] = core[0]
    edges[tail1[-1]] = core[rng.randrange(len(core) // 4)]
    edges[tail2[-1]] = core[rng.randrange(len(core) // 2, len(core))]
    return {"edges": edges, "node1": tail1[0], "node2": tail2[0]}
