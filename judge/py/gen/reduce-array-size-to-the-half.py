"""Reduce Array Size to The Half at n = 10^5 with 2 * 10^4 to 5 * 10^4 distinct values (one seed
skewed, the others close to uniform, so many values must be taken before half the array is gone):
counting each value by a scan costs ~3 * 10^9 comparisons and taking the largest count again for
each value picked costs ~10^9."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5
DISTINCT = (20000, 30000, 50000)


def generate(rng):
    shape = pick_shape(rng)
    values = rng.sample(range(1, N + 1), DISTINCT[shape])
    if shape == 0:
        # Skewed frequencies.
        arr = [
            values[min(int(rng.expovariate(4 / len(values))), len(values) - 1)] for _ in range(N)
        ]
    else:
        arr = [values[rng.randrange(len(values))] for _ in range(N)]
    return {"arr": arr}
