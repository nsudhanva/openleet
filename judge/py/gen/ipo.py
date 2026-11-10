"""IPO with 10^5 projects and k up to 10^5: capital requirements that unlock a few projects at a
time (forcing repeated selection), or everything affordable from the start."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.randrange(3)
    profits = [rng.randint(0, 10**4) for _ in range(N)]
    if shape == 0:
        capital = [rng.randint(0, 10**9) for _ in range(N)]
        w = rng.randint(0, 10**4)
    elif shape == 1:
        capital = [rng.randint(0, 5 * 10**8) for _ in range(N)]
        profits = [rng.randint(5000, 10**4) for _ in range(N)]
        w = 0
        capital[rng.randrange(N)] = 0
    else:
        capital = [0] * N
        w = rng.randint(0, 10**9)
    k = rng.choice([10**5, rng.randint(1, 10**5)])
    return {"k": k, "w": w, "profits": profits, "capital": capital}
