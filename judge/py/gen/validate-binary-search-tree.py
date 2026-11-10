"""Validate BST at 10^4 nodes spanning the full 32-bit range (including -2^31 and 2^31 - 1):
a valid BST, or one deep leaf that obeys its parent but breaks an ancestor's bound or
equals it."""

from _shapes import insert_bst, level_order, pick_shape

SEEDS = 3
N = 10**4
LO, HI = -(2**31), 2**31 - 1


def generate(rng):
    shape = pick_shape(rng)
    values = [*rng.sample(range(LO + 1, HI), N - 2), LO, HI]
    rng.shuffle(values)
    left, right = insert_bst(values, range(N))
    vals = list(values)
    if shape > 0:
        # The deepest leaf whose far-side bound comes from an ancestor (not its parent).
        best = None
        stack = [(0, None, None, 0, None)]
        while stack:
            node, lo, hi, depth, parent = stack.pop()
            if left[node] is None and right[node] is None and parent is not None:
                far = lo if left[parent] == node else hi
                if far is not None and (best is None or depth > best[0]):
                    best = (depth, node, parent, far)
            if left[node] is not None:
                stack.append((left[node], lo, values[node], depth + 1, node))
            if right[node] is not None:
                stack.append((right[node], values[node], hi, depth + 1, node))
        assert best is not None, "the tree has a leaf with a bounded ancestor"
        _, leaf, parent, far = best
        # Equal to the ancestor (invalid under strict ordering), or just past its bound.
        past = far - 1 if far < values[parent] else far + 1
        vals[leaf] = far if shape == 1 or far in (LO, HI) else past
    return {"root": level_order(vals, left, right)}
