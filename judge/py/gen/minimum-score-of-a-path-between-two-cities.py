"""Minimum Score of a Path Between Two Cities at n = 10^5 with 10^5 distinct roads: a long
random tree containing 1 and n plus extra edges, with a smaller-distance road in a separate
component as a trap."""

SEEDS = 3
N = 10**5
ROADS = 10**5


def generate(rng):
    main = rng.randint(N // 2, N - 10)
    others = list(range(2, N))
    rng.shuffle(others)
    comp = [1, N, *others[: main - 2]]
    rest = others[main - 2 :]
    rng.shuffle(comp)
    seen, roads = set(), []

    def add(a, b, low):
        key = (min(a, b), max(a, b))
        if a != b and key not in seen:
            seen.add(key)
            roads.append([a, b, rng.randint(low, 10**4)])

    for i in range(1, len(comp)):
        add(comp[i], comp[rng.randrange(max(0, i - 3), i)], 2)
    for i in range(1, len(rest)):
        add(rest[i], rest[i - 1], 1)
    while len(roads) < ROADS:
        add(rng.choice(comp), rng.choice(comp), 2)
    rng.shuffle(roads)
    return {"n": N, "roads": roads[:ROADS]}
