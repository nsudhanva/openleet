"""Max Sum of Rectangle No Larger Than K on a 100 x 100 matrix (O(m^2 n^2) brute force times
out), with k small, negative, or large."""

SEEDS = 3
N = 100


def generate(rng):
    rows = rng.choice([100, 100, 10])
    matrix = [[rng.randint(-100, 100) for _ in range(N)] for _ in range(rows)]
    k = rng.choice([0, rng.randint(-(10**5), 10**5), rng.randint(-50, 50), 10**5])
    return {"matrix": matrix, "k": k}
