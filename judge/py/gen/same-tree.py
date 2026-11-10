"""Same Tree on 100-node trees (random or a skewed chain): identical, one value changed deep,
or one structural difference."""

from _shapes import level_order, pick_shape, random_tree, shaped_tree

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    n = 100
    left, right = (
        shaped_tree(rng, n, "chain") if rng.random() < 0.4 else random_tree(rng, n, swap=False)
    )
    vals = [rng.randint(-(10**4), 10**4) for _ in range(n)]
    p = level_order(vals, left, right)
    if shape == 0:
        q = list(p)
    elif shape == 1:
        vals2 = list(vals)
        vals2[n - 1] = vals2[n - 1] + 1 if vals2[n - 1] < 10**4 else vals2[n - 1] - 1
        q = level_order(vals2, left, right)
    else:
        # Move the last node to the other side of its parent if free, else drop it.
        left2, right2 = list(left), list(right)
        for parent in range(n):
            if left2[parent] == n - 1:
                left2[parent] = None
                if right2[parent] is None:
                    right2[parent] = n - 1
                break
            if right2[parent] == n - 1:
                right2[parent] = None
                if left2[parent] is None:
                    left2[parent] = n - 1
                break
        q = level_order(vals, left2, right2)
    return {"p": p, "q": q}
