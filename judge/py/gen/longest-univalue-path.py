"""Longest Univalue Path on the maximum 10^4 nodes, one value nearly everywhere, shaped so most
nodes sit near the depth limit of 1000 (a spine with chains or a random tree hanging off its
end): recomputing each node's downward path from scratch is ~9 * 10^6 calls."""

from _shapes import level_order, random_tree

SEEDS = 2
N = 10**4
MAX_DEPTH = 1000


def depths(left, right):
    depth, stack = [1] * len(left), [0]
    while stack:
        node = stack.pop()
        for child in (left[node], right[node]):
            if child is not None:
                depth[child] = depth[node] + 1
                stack.append(child)
    return depth


def comb(rng):
    """A spine to the depth limit; deep spine nodes each grow a chain down to the limit too."""
    left, right = [None] * N, [None] * N
    sides = (left, right)
    for i in range(1, MAX_DEPTH):
        sides[rng.randrange(2)][i - 1] = i
    nxt, top = MAX_DEPTH, MAX_DEPTH - 1
    while nxt < N:
        top -= 1  # spine node top (depth top + 1) grows a chain of MAX_DEPTH - top - 1 nodes
        parent, free = top, 0 if left[top] is None else 1
        for _ in range(MAX_DEPTH - top - 1):
            if nxt == N:
                break
            sides[free][parent] = nxt
            parent, free, nxt = nxt, rng.randrange(2), nxt + 1
    return left, right


def hanging(rng):
    """A random tree of most nodes hung below a spine that leaves it 64 levels."""
    spine = MAX_DEPTH - 64
    while True:
        bl, br = random_tree(rng, N - spine)
        if max(depths(bl, br)) <= MAX_DEPTH - spine:
            break
    left = [None] * spine + [None if c is None else c + spine for c in bl]
    right = [None] * spine + [None if c is None else c + spine for c in br]
    for i in range(1, spine + 1):
        (left if rng.random() < 0.5 else right)[i - 1] = i
    return left, right


def generate(rng):
    if rng.random() < 0.5:
        left, right = comb(rng)
        val = [rng.randint(-1000, 1000)] * len(left)
    else:
        left, right = hanging(rng)
        v = rng.randint(-1000, 999)
        # Leaves sometimes differ, which ends paths without cutting any long one.
        val = [
            v + 1 if left[i] is None and right[i] is None and rng.random() < 0.3 else v
            for i in range(len(left))
        ]
    return {"root": level_order(val, left, right)}
