"""Design HashSet with 10^4 calls over keys up to 10^6: keys colliding modulo common bucket
counts, with adds, removals and membership checks."""

SEEDS = 2
CALLS = 10**4


def generate(rng):
    if rng.random() < 0.5:
        mod = rng.choice([1000, 1024, 769, 10007])
        keys = list(range(rng.randrange(mod), 10**6 + 1, mod))
    else:
        keys = [rng.randint(0, 10**6) for _ in range(3000)]
    ops, args = ["MyHashSet"], [[]]
    for _ in range(CALLS):
        x = rng.random()
        key = rng.choice(keys) if rng.random() < 0.9 else rng.randint(0, 10**6)
        ops.append("add" if x < 0.45 else "remove" if x < 0.6 else "contains")
        args.append([key])
    return {"ops": ops, "args": args}
