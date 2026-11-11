"""Remove Zero Sum Consecutive Nodes from Linked List at the maximum 1000 nodes: positive values
with a few disjoint [-v, v] pairs, so the only zero-sum runs are the pairs and summing forward
from every node costs ~5 * 10^5 steps."""

SEEDS = 2
N = 1000


def generate(rng):
    vals, prefix, seen = [], 0, {0}
    while len(vals) < N:
        v = rng.randint(1, 1000)
        if len(vals) <= N - 3 and rng.random() < 0.05 and prefix - v not in seen:
            vals += [-v, v]
        else:
            prefix += v
            seen.add(prefix)
            vals.append(v)
    return {"head": vals}
