"""H-Index at n = 5000 with citations up to 1000, random or all equal."""

SEEDS = 3
N = 5000


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        citations = [rng.randint(0, 1000) for _ in range(N)]
    elif shape == 1:
        citations = [rng.choice([0, 1000])] * N
    else:
        citations = [rng.randint(0, 20) for _ in range(N)]
    return {"citations": citations}
