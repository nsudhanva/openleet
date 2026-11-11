"""Minimum Fuel Cost to Report to the Capital at n = 2 * 10^4: a long path out of the capital
with one city in ten hung off a random earlier city, so walking each city's route to the capital
is ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    labels = list(range(1, N))
    rng.shuffle(labels)
    labels = [0, *labels]
    roads, tail = [], 0
    for i in range(1, N):
        if rng.random() < 0.9:
            parent, tail = tail, i
        else:
            parent = rng.randrange(i)
        a, b = labels[i], labels[parent]
        roads.append([a, b] if rng.random() < 0.5 else [b, a])
    rng.shuffle(roads)
    return {"roads": roads, "seats": rng.randint(1, 10)}
