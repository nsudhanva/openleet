"""Closest Room. Seed 0 has 2 * 10^4 rooms and the maximum 10^4 queries: small rooms hold one end
of the ids and big ones the other, and most queries prefer the small end but need a big room, so
scanning rooms per query (all of them, the big ones, or outward from the preferred id) costs
~10^8 steps. Most other seeds have 10^5 rooms whose size grows with the id and queries that need
at most 1,000 (so the reference removes few rooms): adding rooms to a sorted list with
bisect.insort in descending size order inserts every id at the front, ~2.7 s a seed against
~0.15 s for the reference."""

from _shapes import pick_shape

SEEDS = 10
N = 2 * 10**4
K = 10**4
LIMIT = 10**7
BIG = 10**5


def generate(rng):
    if pick_shape(rng) != 0:
        return heavy(rng)
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


def heavy(rng):
    ids = sorted(rng.sample(range(1, LIMIT + 1), BIG))
    sizes = sorted(rng.sample(range(1, LIMIT + 1), BIG))
    rooms = [[i, s] for i, s in zip(ids, sizes, strict=True)]
    rng.shuffle(rooms)
    queries = [[rng.randint(1, LIMIT), rng.randint(1, 1000)] for _ in range(K)]
    queries[rng.randrange(K)][1] = 1
    return {"rooms": rooms, "queries": queries}
