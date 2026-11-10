"""K-diff Pairs at n = 10^4 with values in [-10^7, 10^7]: heavy duplicates with k = 0, or a
small value range with k hitting many pairs."""

SEEDS = 3
N = 10**4


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        nums = [rng.randint(-50, 50) for _ in range(N)]
        k = 0
    elif shape == 1:
        nums = [rng.randint(-5000, 5000) for _ in range(N)]
        k = rng.randint(1, 100)
    else:
        nums = [rng.randint(-(10**7), 10**7) for _ in range(N)]
        k = rng.choice([10**7, rng.randint(0, 10**7)])
    return {"nums": nums, "k": k}
