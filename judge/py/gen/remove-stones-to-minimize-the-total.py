"""Remove Stones to Minimize the Total at 10^5 piles and k = 10^5. Seed 0 draws every pile from
the upper half of the range, so each halved pile belongs at the front of a sorted list and keeping
one with bisect.insort moves ~10^5 items per step; other seeds spread the piles over a wide or a
narrow range. Scanning for the largest pile on every operation costs ~10^10 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5
K = 10**5
TOP = 10**4


def generate(rng):
    shape = pick_shape(rng)
    low, high = (TOP // 2 + 1, TOP) if shape == 0 else (1, TOP if shape == 1 else 100)
    return {"piles": [rng.randint(low, high) for _ in range(N)], "k": K}
