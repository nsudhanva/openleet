"""Remove Nodes From Linked List at 3 * 10^4 nodes in non-increasing order (one seed with a few
spikes at the end), so looking right of every node for a greater value costs ~4.5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    vals = sorted((rng.randint(1, 10**5 - 1) for _ in range(N)), reverse=True)
    if rng.random() < 0.5:
        for _ in range(5):
            vals[N - 1 - rng.randrange(N // 100)] = 10**5
    return {"head": vals}
