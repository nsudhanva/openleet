"""Count Complete Tree Nodes on a complete tree of up to 5 * 10^4 nodes: the maximum, a
perfect tree, or a last level only partly filled."""

SEEDS = 3


def generate(rng):
    n = rng.choice([5 * 10**4, 2**15 - 1, rng.randint(2**15, 5 * 10**4)])
    return {"root": [rng.randint(0, 5 * 10**4) for _ in range(n)]}
