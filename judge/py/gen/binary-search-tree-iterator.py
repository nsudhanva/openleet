"""BST Iterator over up to 10^5 distinct values: a right- or left-leaning chain (stack depth
10^5 for the left one) or a random BST, with hasNext/next interleaved up to 10^5 calls and next
only while values remain."""

from _shapes import level_order

SEEDS = 3
CALLS = 10**5


def _bst(rng, n, kind):
    """Shape of a BST over in-order ranks 0..n-1; node id == rank."""
    left, right = [None] * n, [None] * n
    stack = [(0, n, None, 0)]
    root = None
    while stack:
        lo, hi, parent, side = stack.pop()
        if lo >= hi:
            continue
        if kind == "right":
            mid = lo
        elif kind == "left":
            mid = hi - 1
        else:
            mid = rng.randrange(lo, hi)
        if parent is None:
            root = mid
        else:
            (left, right)[side][parent] = mid
        stack.append((lo, mid, mid, 0))
        stack.append((mid + 1, hi, mid, 1))
    return root, left, right


def generate(rng):
    kind = rng.choice(["right", "left", "random"])
    n = rng.choice([5 * 10**4, 10**5]) if kind == "random" else 5 * 10**4
    root, left, right = _bst(rng, n, kind)
    vals = sorted(rng.sample(range(10**6 + 1), n))
    # Relabel so the root is node 0, as _level_order expects.
    order = [root]
    i = 0
    while i < len(order):
        node = order[i]
        i += 1
        for child in (left[node], right[node]):
            if child is not None:
                order.append(child)
    new = {old: k for k, old in enumerate(order)}
    nl = [None if left[old] is None else new[left[old]] for old in order]
    nr = [None if right[old] is None else new[right[old]] for old in order]
    nv = [vals[old] for old in order]
    ops, args = ["BSTIterator"], [[level_order(nv, nl, nr)]]
    remaining = n
    while len(ops) - 1 < CALLS:
        if remaining and rng.random() < 0.7:
            ops.append("next")
            remaining -= 1
        else:
            ops.append("hasNext")
        args.append([])
    return {"ops": ops, "args": args}
