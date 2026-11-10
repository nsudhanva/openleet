"""Linked List Cycle on 10^4 nodes: a cycle back to a random node, or no cycle at all."""

SEEDS = 3
N = 10**4


def generate(rng):
    head = [rng.randint(-(10**5), 10**5) for _ in range(N)]
    pos = rng.choice([-1, 0, rng.randrange(N), N - 1])
    return {"head": head, "pos": pos}
