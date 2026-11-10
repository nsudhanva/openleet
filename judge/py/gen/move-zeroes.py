"""Move Zeroes at n = 10^4 with half zeros (or zeros all at the front), values across the
full 32-bit range; removing zeros one by one is quadratic."""

SEEDS = 3
N = 10**4


def generate(rng):
    if rng.random() < 0.5:
        zeros = rng.randint(N // 2, N - 1)
        nums = [0] * zeros + [rng.randint(-(2**31), 2**31 - 1) or 1 for _ in range(N - zeros)]
    else:
        nums = [0 if rng.random() < 0.5 else rng.randint(-(2**31), 2**31 - 1) for _ in range(N)]
    return {"nums": nums}
