"""Minimum Index Sum of Two Lists with 1000 unique restaurant names in each list and a
random overlap (at least one shared name), so nested comparison is 10^6 string checks."""

from string import ascii_letters

from _shapes import random_string

SEEDS = 3


def name(rng):
    words = [random_string(rng, ascii_letters, rng.randint(1, 8)) for _ in range(rng.randint(1, 3))]
    return " ".join(words)[:30].strip()


def generate(rng):
    pool = set()
    while len(pool) < 2000:
        pool.add(name(rng))
    pool = sorted(pool)
    rng.shuffle(pool)
    shared = rng.choice((1, 100, 1000))
    common = pool[:shared]
    list1 = common + pool[shared : shared + 1000 - shared]
    rest = pool[1000:]
    list2 = common + rest[: 1000 - shared]
    rng.shuffle(list1)
    rng.shuffle(list2)
    return {"list1": list1, "list2": list2}
