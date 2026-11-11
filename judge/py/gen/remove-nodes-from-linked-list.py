"""Remove Nodes From Linked List at 3 * 10^4 nodes in non-increasing order, in one seed with a few
spikes at the end. Without spikes everything stays, so looking right of every node for a greater
value costs ~4.5 * 10^8 steps; with them nearly every node goes, one per pass, so repeated
removal passes cost ~9 * 10^8 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 3 * 10**4


def generate(rng):
    spikes = pick_shape(rng) == 1
    vals = sorted((rng.randint(1, 10**5 - 1) for _ in range(N)), reverse=True)
    if spikes:
        for _ in range(5):
            vals[N - 1 - rng.randrange(N // 100)] = 10**5
    return {"head": vals}
