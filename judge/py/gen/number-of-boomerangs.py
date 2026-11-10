"""Number of Boomerangs with 500 unique points: packed on a small lattice so many distances
repeat (O(n^3) checks are 1.25 * 10^8), or spread over [-10^4, 10^4]."""

SEEDS = 3
N = 500


def generate(rng):
    half = rng.choice((12, 10**4))
    side = 2 * half + 1
    cells = rng.sample(range(side * side), N)
    return {"points": [[c // side - half, c % side - half] for c in cells]}
