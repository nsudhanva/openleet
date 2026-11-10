"""Sort List at 5 * 10^4 nodes: random, reverse sorted, or few distinct values."""

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    shape = rng.getrandbits(6) % 3
    if shape == 0:
        head = [rng.randint(-(10**5), 10**5) for _ in range(N)]
    elif shape == 1:
        head = sorted((rng.randint(-(10**5), 10**5) for _ in range(N)), reverse=True)
    else:
        head = [rng.randint(-2, 2) for _ in range(N)]
    return {"head": head}
