"""Can Place Flowers at length 2 * 10^4 with no two adjacent flowers: sparse or empty beds,
with n just at or just above the number that fits."""

SEEDS = 3
N = 2 * 10**4


def generate(rng):
    bed = [0] * N
    density = rng.choice([0.0, 0.05, 0.3])
    for i in range(N):
        if rng.random() < density and (i == 0 or bed[i - 1] == 0):
            bed[i] = 1
    # Greedy count of what fits, to place n right at the boundary.
    fit, prev = 0, list(bed)
    for i in range(N):
        if prev[i] == 0 and (i == 0 or prev[i - 1] == 0) and (i == N - 1 or prev[i + 1] == 0):
            prev[i] = 1
            fit += 1
    n = min(N, max(0, fit + rng.choice([0, 1, -1])))
    return {"flowerbed": bed, "n": n}
