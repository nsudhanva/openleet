"""H-Index II on 10^5 sorted citations up to 1000 (the answer is capped near 1000 while n is
large), or all zeros."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        citations = sorted(rng.randint(0, 1000) for _ in range(N))
    elif shape == 1:
        citations = [0] * N
    else:
        citations = sorted(rng.randint(0, 1000) if rng.random() < 0.01 else 0 for _ in range(N))
    return {"citations": citations}
