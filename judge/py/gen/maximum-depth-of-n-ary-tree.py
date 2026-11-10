"""Maximum Depth of N-ary Tree with 10^4 nodes: 1000 levels of about ten nodes each (the depth
limit), or a bushy tree with uneven branching."""

import itertools

SEEDS = 2
N = 10**4


def generate(rng):
    if rng.random() < 0.5:
        sizes = [1] + [10] * 999
    else:
        sizes = [1]
        while sum(sizes) < N:
            sizes.append(min(N - sum(sizes), rng.randint(1, sizes[-1] * 5)))
    # Distribute each level's nodes among the previous level's parents (children are grouped
    # by parent in BFS order).
    children = []  # children[node] = count, in BFS order
    for level in range(len(sizes) - 1):
        cuts = sorted(rng.randint(0, sizes[level + 1]) for _ in range(sizes[level] - 1))
        bounds = [0, *cuts, sizes[level + 1]]
        children.extend(b - a for a, b in itertools.pairwise(bounds))
    children.extend([0] * sizes[-1])
    total = sum(sizes)
    vals = [rng.randint(0, 10**4) for _ in range(total)]
    out = [vals[0], None]
    nxt = 1
    for node in range(total):
        out.extend(vals[nxt : nxt + children[node]])
        nxt += children[node]
        out.append(None)
    while out and out[-1] is None:
        out.pop()
    return {"root": out}
