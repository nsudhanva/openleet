"""RLE Iterator with a 1000-entry encoding (huge counts, many zero runs) and 1000 next calls of
small and huge sizes, so per-unit expansion is hopeless."""

SEEDS = 2


def generate(rng):
    encoding = []
    for _ in range(500):
        count = 0 if rng.random() < 0.3 else rng.choice([rng.randint(1, 10), rng.randint(1, 10**9)])
        encoding += [count, rng.randint(0, 10**9)]
    ops, args = ["RLEIterator"], [[encoding]]
    for _ in range(1000):
        ops.append("next")
        args.append([rng.choice([rng.randint(1, 5), rng.randint(1, 10**6), rng.randint(1, 10**9)])])
    return {"ops": ops, "args": args}
