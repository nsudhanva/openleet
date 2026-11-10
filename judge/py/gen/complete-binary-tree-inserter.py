"""CBT Inserter from a 1000-node complete tree followed by ~10^4 inserts (and a few get_root
calls), so re-walking the tree on every insert is quadratic."""

SEEDS = 2
CALLS = 10**4


def generate(rng):
    n = rng.choice([1000, rng.randint(1, 1000)])
    root = [rng.randint(0, 5000) for _ in range(n)]
    ops, args = ["CBTInserter"], [[root]]
    roots_at = {CALLS // 2, CALLS - 1}
    for i in range(CALLS):
        if i in roots_at:
            ops.append("get_root")
            args.append([])
        else:
            ops.append("insert")
            args.append([rng.randint(0, 5000)])
    return {"ops": ops, "args": args}
