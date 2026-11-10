"""Positions of Large Groups at length 1000 with many runs of length 2 to 6 around the
threshold of 3."""

SEEDS = 2


def generate(rng):
    s, prev = [], ""
    while len(s) < 1000:
        c = rng.choice([x for x in "abc" if x != prev])
        s.extend(c * rng.randint(1, 6))
        prev = c
    return {"s": "".join(s[:1000])}
