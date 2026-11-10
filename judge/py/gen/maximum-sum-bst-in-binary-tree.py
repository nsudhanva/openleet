"""Maximum Sum BST in Binary Tree at 4 * 10^4 nodes: a skewed valid BST chain (deep
recursion), a random-shape BST with a few corrupted values, and a random tree."""

from collections import deque

SEEDS = 3
N = 4 * 10**4
LIMIT = 4 * 10**4


def shape(rng, n, skew):
    """Children of a random binary tree whose in-order is 0..n-1; returns (root, left, right)."""
    left, right = [None] * n, [None] * n
    stack = [(0, n - 1, None, False)]
    root = None
    while stack:
        lo, hi, parent, is_right = stack.pop()
        if lo > hi:
            continue
        mid = lo if skew else rng.randint(lo, hi)
        if parent is None:
            root = mid
        elif is_right:
            right[parent] = mid
        else:
            left[parent] = mid
        stack.append((lo, mid - 1, mid, False))
        stack.append((mid + 1, hi, mid, True))
    return root, left, right


def level_order(root, vals, left, right):
    out, queue = [], deque([root])
    while queue:
        i = queue.popleft()
        if i is None:
            out.append(None)
            continue
        out.append(vals[i])
        queue.append(left[i])
        queue.append(right[i])
    while out and out[-1] is None:
        out.pop()
    return out


def generate(rng):
    kind = rng.choice(("chain", "corrupt", "random"))
    if kind == "random":
        root, left, right = shape(rng, N, False)
        vals = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    else:
        root, left, right = shape(rng, N, kind == "chain")
        vals = sorted(rng.sample(range(-LIMIT, LIMIT + 1), N))
        if kind == "corrupt":
            for _ in range(20):
                vals[rng.randrange(N)] = rng.randint(-LIMIT, LIMIT)
    return {"root": level_order(root, vals, left, right)}
