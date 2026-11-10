"""Insertion Sort List at the maximum 5000 nodes: reverse sorted, already sorted, or random with
many duplicates."""

SEEDS = 3
N = 5000


def generate(rng):
    head = [rng.randint(-5000, 5000) for _ in range(N)]
    shape = rng.randrange(3)
    if shape == 0:
        head.sort(reverse=True)
    elif shape == 1:
        head.sort()
    else:
        head = [rng.randint(-3, 3) for _ in range(N)]
    return {"head": head}
