"""Symmetric Tree at 999 nodes: a random half mirrored (true), or the same with one value or
one child moved deep in the tree (false at the last comparison)."""

from _shapes import level_order, pick_shape

SEEDS = 3
HALF = 499


def generate(rng):
    shape = pick_shape(rng)
    # Build the left half as parallel arrays, then mirror it.
    left, right = [None] * HALF, [None] * HALF
    slots = [(0, 0), (0, 1)]
    for v in range(1, HALF):
        if rng.random() < 0.3:
            parent, side = v - 1, rng.randrange(2)  # bias toward long paths
            if (left if side == 0 else right)[parent] is not None:
                parent, side = None, None
        else:
            parent = None
        if parent is None:
            j = rng.randrange(len(slots))
            slots[j], slots[-1] = slots[-1], slots[j]
            parent, side = slots.pop()
        else:
            slots.remove((parent, side))
        (left if side == 0 else right)[parent] = v
        slots.append((v, 0))
        slots.append((v, 1))
    vals = [rng.randint(-100, 100) for _ in range(HALF)]
    # Nodes: 0 = root, 1..HALF = left copy, HALF+1..2*HALF = mirrored copy.
    total = 2 * HALF + 1
    tv, tl, tr = [0] * total, [None] * total, [None] * total
    tv[0] = rng.randint(-100, 100)
    tl[0], tr[0] = 1, HALF + 1
    for v in range(HALF):
        a, b = 1 + v, HALF + 1 + v
        tv[a] = tv[b] = vals[v]
        tl[a] = None if left[v] is None else 1 + left[v]
        tr[a] = None if right[v] is None else 1 + right[v]
        tl[b] = None if right[v] is None else HALF + 1 + right[v]
        tr[b] = None if left[v] is None else HALF + 1 + left[v]
    if shape == 1:
        node = HALF + 1 + rng.randrange(HALF)
        tv[node] = tv[node] + 1 if tv[node] < 100 else tv[node] - 1
    elif shape == 2:
        leaves = [v for v in range(HALF + 1, total) if tl[v] is None and tr[v] is None]
        node = rng.choice(leaves)
        # Swap a child slot of the leaf's parent so the shape breaks symmetry.
        parent = next(p for p in range(total) if tl[p] == node or tr[p] == node)
        tl[parent], tr[parent] = tr[parent], tl[parent]
        if tl[parent] is not None and tr[parent] is not None:
            tv[node] = tv[node] + 1 if tv[node] < 100 else tv[node] - 1
    return {"root": level_order(tv, tl, tr)}
