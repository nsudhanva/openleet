"""Compressed String Iterator on a 1000-character string of ~100 runs, most repeated close to
10^9 times, with 100 calls crossing the short runs first, so expanding the string up front needs
~10^11 characters."""

SEEDS = 2
LENGTH = 1000
TOP = 10**9


def generate(rng):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    parts, size, short = [], 0, rng.randint(5, 15)
    while True:
        count = rng.randint(1, 4) if len(parts) < short else rng.randint(TOP - TOP // 10, TOP)
        part = rng.choice(letters) + str(count)
        if size + len(part) > LENGTH:
            break
        parts.append(part)
        size += len(part)
    ops, args = ["StringIterator"], [["".join(parts)]]
    for _ in range(100):
        ops.append("next" if rng.random() < 0.7 else "hasNext")
        args.append([])
    return {"ops": ops, "args": args}
