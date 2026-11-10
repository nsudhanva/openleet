"""All O`one at 5 * 10^4 calls: many inc/dec on a key pool so counts climb high and keys keep
moving between buckets, with frequent max/min queries; dec only on keys present."""

from _shapes import random_string

SEEDS = 2
CALLS = 5 * 10**4
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    pool = set()
    size = rng.choice([20, 2000])
    while len(pool) < size:
        pool.add(random_string(rng, LETTERS, rng.randint(1, 10)))
    pool = sorted(pool)
    counts = {}
    present = []  # keys with count > 0, in insertion order, for deterministic choice
    ops, args = ["AllOne"], [[]]
    for _ in range(CALLS):
        r = rng.random()
        if r < 0.45 or not present:
            key = rng.choice(pool) if rng.random() < 0.5 or not present else rng.choice(present)
            if counts.get(key, 0) == 0:
                present.append(key)
            counts[key] = counts.get(key, 0) + 1
            ops.append("inc")
            args.append([key])
        elif r < 0.7:
            key = rng.choice(present)
            counts[key] -= 1
            if counts[key] == 0:
                present.remove(key)
            ops.append("dec")
            args.append([key])
        else:
            ops.append(rng.choice(["getMaxKey", "getMinKey"]))
            args.append([])
    return {"ops": ops, "args": args}
