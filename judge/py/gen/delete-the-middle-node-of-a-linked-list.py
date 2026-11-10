"""Delete the Middle Node of a Linked List at the maximum 10^5 nodes (odd or even length)."""

SEEDS = 2


def generate(rng):
    n = rng.choice([10**5, 10**5 - 1])
    return {"head": [rng.randint(1, 10**5) for _ in range(n)]}
