"""Time Based Key-Value Store with 1.8 * 10^5 calls: few keys with long histories so lookups
must binary search, gets before, between and after the stored timestamps."""

from string import ascii_lowercase, digits

from _shapes import random_string

SEEDS = 2
CALLS = 18 * 10**4
CHARS = ascii_lowercase + digits


def generate(rng):
    keys = sorted({random_string(rng, CHARS, rng.randint(1, 5)) for _ in range(20)})
    ops, args = ["TimeMap"], [[]]
    ts = 0
    for _ in range(CALLS):
        if rng.random() < 0.5 and ts < 10**7 - 50:
            ts += rng.randint(1, 50)
            value = random_string(rng, CHARS, rng.randint(1, 5))
            ops.append("set")
            args.append([rng.choice(keys), value, ts])
        else:
            ops.append("get")
            args.append([rng.choice(keys), rng.randint(1, min(10**7, ts + 100))])
    return {"ops": ops, "args": args}
