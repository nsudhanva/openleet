"""Boats to Save People at n = 5 * 10^4: random weights, or weights near limit / 2 where pairing
choices matter, with limit up to 3 * 10^4."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    limit = rng.randint(2, 3 * 10**4)
    if rng.random() < 0.5:
        people = [rng.randint(1, limit) for _ in range(N)]
    else:
        half = limit // 2
        people = [max(1, min(limit, half + rng.randint(-3, 3))) for _ in range(N)]
    return {"people": people, "limit": limit}
