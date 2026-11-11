"""2 to 5 students using 1 or 2 pieces each and k near 10^9, so handing out chalk turn by
turn, or even a whole round at a time, takes 10^8 steps or more."""

SEEDS = 2


def generate(rng):
    n = rng.randint(2, 5)
    return {"chalk": [rng.randint(1, 2) for _ in range(n)], "k": rng.randint(9 * 10**8, 10**9)}
