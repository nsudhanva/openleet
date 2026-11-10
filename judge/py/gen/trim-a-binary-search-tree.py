"""Trim a BST at 10^4 nodes: a fully degenerate chain (deep recursion) or a random insertion
BST, with low/high cutting through the middle."""

import itertools

SEEDS = 3
N = 10**4
TOP = 10**4


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    values = rng.sample(range(TOP + 1), N)
    if shape == 0:
        values.sort()
    elif shape == 1:
        values.sort(reverse=True)
    left, right = {}, {}
    root = values[0]
    if values == sorted(values):
        right = dict(itertools.pairwise(values))  # inserting sorted values is a right chain
    elif values == sorted(values, reverse=True):
        left = dict(itertools.pairwise(values))
    for v in values[1:] if not (left or right) else []:
        cur = root
        while True:
            side = left if v < cur else right
            if cur in side:
                cur = side[cur]
            else:
                side[cur] = v
                break
    out, queue, i = [], [root], 0
    while i < len(queue):
        node = queue[i]
        i += 1
        if node is None:
            out.append(None)
            continue
        out.append(node)
        queue.append(left.get(node))
        queue.append(right.get(node))
    while out and out[-1] is None:
        out.pop()
    a, b = rng.randint(0, TOP), rng.randint(0, TOP)
    return {"root": out, "low": min(a, b), "high": max(a, b)}
