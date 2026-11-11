"""Closest Room with 2 * 10^4 rooms and the maximum 10^4 queries: small rooms hold one end of the
ids and big ones the other, and most queries prefer the small end but need a big room, so scanning
rooms per query (all of them, the big ones, or outward from the preferred id) costs ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4
K = 10**4
LIMIT = 10**7


def generate(rng):
    ids = sorted(rng.sample(range(1, LIMIT + 1), N))
    half = LIMIT // 2
    sizes = [rng.randint(1, half) for _ in range(N // 2)]
    sizes += [rng.randint(half + 1, LIMIT) for _ in range(N - N // 2)]
    near = (1, ids[N // 10])
    if rng.random() < 0.5:
        sizes.reverse()
        near = (ids[N - N // 10], LIMIT)
    rooms = [[i, s] for i, s in zip(ids, sizes, strict=True)]
    rng.shuffle(rooms)
    biggest = max(sizes)
    queries = []
    for _ in range(K):
        roll = rng.random()
        if roll < 0.02 and biggest < LIMIT:
            queries.append([rng.randint(1, LIMIT), biggest + 1])
        elif roll < 0.12:
            queries.append([rng.randint(1, LIMIT), rng.randint(1, biggest)])
        else:
            queries.append([rng.randint(*near), rng.randint(half + 1, biggest)])
    return {"rooms": rooms, "queries": queries}
