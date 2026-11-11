"""Remove Stones to Minimize the Total at 2 * 10^4 piles and k = 2 * 10^4, so finding the largest
pile by a scan on every operation costs ~4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
K = 2 * 10**4


def generate(rng):
    top = rng.choice((10**4, 100))
    return {"piles": [rng.randint(1, top) for _ in range(N)], "k": K}
