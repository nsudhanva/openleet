"""Two Non-overlapping Sub-arrays with Target Sum at n = 10^5: small values and a target hit by
many windows, or all-ones where only two halves fit."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        arr = [rng.randint(1, 1000) for _ in range(N)]
        target = rng.randint(1000, 5000)
    elif shape == 1:
        arr = [1] * N
        target = rng.choice([N // 2, N // 2 - 1, N // 2 + 1])
    else:
        arr = [rng.randint(1, 3) for _ in range(N)]
        target = rng.randint(50, 500)
    return {"arr": arr, "target": target}
