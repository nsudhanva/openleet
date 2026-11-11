"""Max Stack at 6.8 * 10^4 calls: 3.4 * 10^4 pushes of falling values, then mostly popMax with a
few peekMax, pop and top and a push of a negative value after each removal, so the max always sits
at the bottom of a ~3.4 * 10^4 deep stack and scanning for it per removal is ~5 * 10^8 steps."""

SEEDS = 2
CALLS = 68 * 10**3
TOP = 10**6
BELOW = 99


def generate(rng):
    ops, args = ["MaxStack"], [[]]
    depth = CALLS // 2
    for x in sorted(rng.sample(range(TOP), depth), reverse=True):
        ops.append("push")
        args.append([x])
    while len(ops) - 1 + 2 <= CALLS:
        op = rng.choices(["popMax", "peekMax", "pop", "top"], [30, 1, 1, 1])[0]
        ops.append(op)
        args.append([])
        if op in ("popMax", "pop"):
            ops.append("push")
            args.append([-rng.randint(1, BELOW)])
    return {"ops": ops, "args": args}
