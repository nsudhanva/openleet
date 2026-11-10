"""Largest Rectangle in Histogram at n = 10^5: strictly increasing heights (worst case for
expanding from each bar), all-equal bars, or random heights."""

SEEDS = 3
N = 10**5
LIMIT = 10**4


def generate(rng):
    shape = rng.choice(["increasing", "equal", "random"])
    if shape == "increasing":
        heights = sorted(rng.randint(0, LIMIT) for _ in range(N))
    elif shape == "equal":
        heights = [rng.randint(1, LIMIT)] * N
    else:
        heights = [rng.randint(0, LIMIT) for _ in range(N)]
    return {"heights": heights}
