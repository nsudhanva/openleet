"""Koko Eating Bananas with 10^4 piles up to 10^9 each, so a linear scan over speeds times
out; one seed makes h equal to the pile count (speed = max pile)."""

SEEDS = 3
N = 10**4


def generate(rng):
    piles = [rng.randint(1, 10**9) for _ in range(N)]
    shape = rng.choice(["tight", "loose", "mid"])
    if shape == "tight":
        h = N
    elif shape == "loose":
        h = rng.randint(10**9 - 1000, 10**9)
    else:
        h = rng.randint(N, 10**9)
    return {"piles": piles, "h": h}
