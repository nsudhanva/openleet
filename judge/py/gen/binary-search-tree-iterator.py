"""BST Iterator over up to 10^5 distinct values: a right- or left-leaning chain (stack depth
10^5 for the left one) or a random BST, with hasNext/next interleaved up to 10^5 calls and next
only while values remain."""

from _shapes import level_order, random_bst

SEEDS = 3
CALLS = 10**5


def generate(rng):
    kind = rng.choice(["right", "left", "random"])
    n = rng.choice([5 * 10**4, 10**5]) if kind == "random" else 5 * 10**4
    root, left, right = random_bst(rng, n, None if kind == "random" else kind)
    vals = sorted(rng.sample(range(10**6 + 1), n))
    ops, args = ["BSTIterator"], [[level_order(vals, left, right, root)]]
    remaining = n
    while len(ops) - 1 < CALLS:
        if remaining and rng.random() < 0.7:
            ops.append("next")
            remaining -= 1
        else:
            ops.append("hasNext")
        args.append([])
    return {"ops": ops, "args": args}
