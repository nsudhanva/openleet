"""Reverse Nodes in k-Group at n = 5000 with k = 1, 2, n, or a random k that leaves a tail."""

SEEDS = 3


def generate(rng):
    n = 5000
    head = [rng.randint(0, 1000) for _ in range(n)]
    k = rng.choice([2, n, rng.randint(3, n - 1), rng.randint(3, 100)])
    return {"head": head, "k": k}
