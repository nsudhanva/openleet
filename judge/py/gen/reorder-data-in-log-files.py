"""Reorder Log Files at the maximum 100 logs, many letter-logs with identical contents so ties
must break by identifier, mixed with digit-logs."""

from _shapes import random_string

SEEDS = 2
VOCAB = ["art", "can", "zero", "own", "kit", "dig", "act", "car", "zoo", "off", "key"]


def generate(rng):
    ids = set()
    while len(ids) < 100:
        n = rng.randint(1, 4)
        ids.add(rng.choice("abcdefghij") + random_string(rng, "abc0123456789", n - 1))
    ids = sorted(ids)
    rng.shuffle(ids)
    contents = [" ".join(rng.choice(VOCAB) for _ in range(rng.randint(1, 3))) for _ in range(5)]
    logs = []
    for ident in ids:
        if rng.random() < 0.6:
            body = (
                rng.choice(contents)
                if rng.random() < 0.7
                else " ".join(rng.choice(VOCAB) for _ in range(rng.randint(1, 10)))
            )
        else:
            body = " ".join(str(rng.randint(0, 999)) for _ in range(rng.randint(1, 10)))
        logs.append(f"{ident} {body}")
    return {"logs": logs}
