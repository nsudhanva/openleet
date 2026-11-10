"""Design HashMap with 10^4 calls over keys up to 10^6: keys colliding modulo common bucket
counts, with updates, removals and lookups of present and absent keys."""

SEEDS = 2
CALLS = 10**4


def generate(rng):
    if rng.random() < 0.5:
        mod = rng.choice([1000, 1024, 769, 10007])
        keys = list(range(rng.randrange(mod), 10**6 + 1, mod))
    else:
        keys = [rng.randint(0, 10**6) for _ in range(3000)]
    ops, args = ["MyHashMap"], [[]]
    for _ in range(CALLS):
        x = rng.random()
        key = rng.choice(keys) if rng.random() < 0.9 else rng.randint(0, 10**6)
        if x < 0.45:
            ops.append("put")
            args.append([key, rng.randint(0, 10**6)])
        elif x < 0.6:
            ops.append("remove")
            args.append([key])
        else:
            ops.append("get")
            args.append([key])
    return {"ops": ops, "args": args}
