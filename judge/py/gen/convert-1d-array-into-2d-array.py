"""Convert 1D Array Into 2D Array with 5 * 10^4 elements: a fitting m x n shape, or one whose
product does not match."""

SEEDS = 3
L = 5 * 10**4


def generate(rng):
    original = [rng.randint(1, 10**5) for _ in range(L)]
    shape = rng.randrange(3)
    if shape == 0:
        m, n = 200, 250
    elif shape == 1:
        m, n = 2, L // 2
    else:
        m, n = rng.randint(1, 4 * 10**4), rng.randint(1, 4 * 10**4)
    if rng.random() < 0.5:
        m, n = n, m
    return {"original": original, "m": m, "n": n}
