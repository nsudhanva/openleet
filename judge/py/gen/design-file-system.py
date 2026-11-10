"""Design File System with 10^4 calls building deep paths (up to 100 characters), mixing
valid creations, duplicates, missing parents, and lookups of present and absent paths."""

from _shapes import random_string

SEEDS = 2
CALLS = 10**4
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def name(rng):
    return random_string(rng, LETTERS, rng.randint(1, 4))


def generate(rng):
    created = []
    ops, args = ["FileSystem"], [[]]
    for _ in range(CALLS):
        x = rng.random()
        if x < 0.5:
            parent = rng.choice(created) if created and rng.random() < 0.9 else ""
            if rng.random() < 0.1:
                parent += "/" + name(rng)
            path = parent + "/" + name(rng)
            if len(path) > 100:
                path = "/" + name(rng)
            if rng.random() < 0.05 and created:
                path = rng.choice(created)
            ops.append("createPath")
            args.append([path, rng.randint(1, 10**9)])
            created.append(path)
        else:
            if created and rng.random() < 0.7:
                path = rng.choice(created)
            else:
                path = "/" + name(rng) + "/" + name(rng)
            ops.append("get")
            args.append([path])
    return {"ops": ops, "args": args}
