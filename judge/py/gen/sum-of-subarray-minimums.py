"""Sum of Subarray Minimums at n = 3 * 10^4: sorted, reverse sorted, all equal (ties) or
random, the cases that break naive and tie-mishandling stack solutions."""

SEEDS = 3
N = 3 * 10**4


def generate(rng):
    shape = rng.randrange(4)
    if shape == 0:
        arr = sorted(rng.randint(1, N) for _ in range(N))
    elif shape == 1:
        arr = sorted((rng.randint(1, N) for _ in range(N)), reverse=True)
    elif shape == 2:
        arr = [rng.randint(1, 3) for _ in range(N)]
    else:
        arr = [rng.randint(1, N) for _ in range(N)]
    return {"arr": arr}
