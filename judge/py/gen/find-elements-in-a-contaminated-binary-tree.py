"""Find Elements in a Contaminated Binary Tree with 10^4 nodes (depth at most 20) and 10^4 find
calls, most for absent values, so searching the recovered tree on each call is ~10^8 steps."""

from _shapes import level_order

SEEDS = 2
N = 10**4
CALLS = 10**4
DEPTH = 20


def generate(rng):
    left, right = [None] * N, [None] * N
    value = [0] * N
    slots = [(0, 0, 1), (0, 1, 1)]
    for i in range(1, N):
        # A random open slot; slots on the deepest level allowed take no children.
        j = rng.randrange(len(slots))
        slots[j], slots[-1] = slots[-1], slots[j]
        parent, side, depth = slots.pop()
        (left, right)[side][parent] = i
        value[i] = 2 * value[parent] + 1 + side
        if depth + 1 < DEPTH:
            slots += [(i, 0, depth + 1), (i, 1, depth + 1)]
    present = [v for v in value if v <= 10**6]
    ops, args = ["FindElements"], [[level_order([-1] * N, left, right)]]
    for _ in range(CALLS):
        ops.append("find")
        args.append([rng.choice(present) if rng.random() < 0.2 else rng.randint(0, 10**6)])
    return {"ops": ops, "args": args}
