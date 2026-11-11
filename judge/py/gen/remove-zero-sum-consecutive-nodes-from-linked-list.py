"""Remove Zero Sum Consecutive Nodes from Linked List at the maximum 1000 nodes: 300 to 600
positive values, then disjoint [-v, v] pairs (about 5% of the values after that are single
positives), so the only zero-sum runs are the pairs, all of them at the end of the list: summing
forward from every node costs ~5 * 10^5 steps and re-scanning for a repeated prefix sum after
each removal costs ~10^8."""

SEEDS = 4
N = 1000
HEAD = (300, 600)


def generate(rng):
    vals, prefix, seen = [], 0, {0}
    head = rng.randint(*HEAD)
    while len(vals) < N:
        v = rng.randint(1, 1000)
        if head <= len(vals) <= N - 3 and rng.random() < 0.95 and prefix - v not in seen:
            vals += [-v, v]
        else:
            prefix += v
            seen.add(prefix)
            vals.append(v)
    return {"head": vals}
