"""Dinner Plate Stacks with 6 * 10^4 calls: 3 * 10^4 pushes onto stacks of capacity 1 or 2, then
cycles of popAtStack on a low stack, two pushes and a pop, so each second push must find the
leftmost open stack past a full row: a scan for it is ~5 * 10^8 steps."""

SEEDS = 2
PUSHES = 3 * 10**4
CALLS = 6 * 10**4


def generate(rng):
    capacity = rng.randint(1, 2)
    ops, args = ["DinnerPlates"], [[capacity]]
    for _ in range(PUSHES):
        ops.append("push")
        args.append([rng.randint(1, 2 * 10**4)])
    low = min(PUSHES // capacity, 1000)
    while len(ops) + 4 <= CALLS + 1:
        ops += ["popAtStack", "push", "push", "pop"]
        args += [[rng.randrange(low)], [rng.randint(1, 2 * 10**4)], [rng.randint(1, 2 * 10**4)], []]
    return {"ops": ops, "args": args}
