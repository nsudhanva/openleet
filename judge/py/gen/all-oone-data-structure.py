"""All O`one at 5 * 10^4 calls: 1.2 * 10^4 keys raised to count 2, then one key above them
and one below take inc/dec between ~1.7 * 10^4 max/min queries, so scanning every key per
query is ~2 * 10^8 steps; the max and min key are always unique."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
CALLS = 5 * 10**4
KEYS = 12000


def generate(rng):
    pool = set()
    while len(pool) < KEYS + 2:
        pool.add(random_string(rng, ascii_lowercase, rng.randint(1, 10)))
    pool = sorted(pool)
    rng.shuffle(pool)
    top, bottom, bulk = pool[0], pool[1], pool[2:]
    build = [*bulk, *bulk, top, top, top, bottom]
    rng.shuffle(build)
    ops, args = ["AllOne"], [[]]
    for key in build:
        ops.append("inc")
        args.append([key])
    count = 3  # the top key's count; the bulk sits at 2 and the bottom key at 1
    while len(ops) - 1 + 3 <= CALLS:
        if count > 3 and rng.random() < 0.3:
            ops.append("dec")
            count -= 1
        else:
            ops.append("inc")
            count += 1
        args.append([top])
        for query in rng.sample(["getMaxKey", "getMinKey"], 2):
            ops.append(query)
            args.append([])
    return {"ops": ops, "args": args}
