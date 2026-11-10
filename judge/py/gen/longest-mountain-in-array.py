"""Longest Mountain at n = 10^4: one huge mountain spanning the array, plateaus that break
mountains, or random values."""

SEEDS = 3
N = 10**4


def generate(rng):
    shape = rng.choice(["one", "plateau", "random"])
    if shape == "one":
        peak = rng.randint(1, N - 2)
        up = sorted(rng.sample(range(0, 10**4), peak))
        down = sorted(rng.sample(range(0, 10**4), N - peak - 1), reverse=True)
        arr = [*up, 10**4, *down]
    elif shape == "plateau":
        arr = [rng.randint(0, 3) for _ in range(N)]
    else:
        arr = [rng.randint(0, 10**4) for _ in range(N)]
    return {"arr": arr}
