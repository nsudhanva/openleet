"""Candy at n = 5 * 10^4: strictly increasing or decreasing ratings (the candy counts grow to n),
long mountains and valleys, or random ratings with ties."""

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    shape = rng.choice(["increasing", "decreasing", "mountains", "random"])
    if shape == "increasing":
        ratings = list(range(N))
    elif shape == "decreasing":
        ratings = list(range(N, 0, -1))
    elif shape == "mountains":
        width = rng.randint(100, 5000)
        ratings = [abs((i % (2 * width)) - width) for i in range(N)]
    else:
        ratings = [rng.randint(0, 5 * 10**4) for _ in range(N)]
    return {"ratings": ratings}
