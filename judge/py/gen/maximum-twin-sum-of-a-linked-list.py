"""Maximum Twin Sum of a Linked List at 3 * 10^4 nodes, so walking from the head to each node's
twin costs ~3 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    return {"head": [rng.randint(1, 10**5) for _ in range(N)]}
