"""Can Make Arithmetic Progression at length 1000: a shuffled progression (true), the same with
one value nudged (false), or all equal values."""

SEEDS = 3
N = 1000


def generate(rng):
    shape = rng.choice(["ap", "broken", "equal"])
    if shape == "equal":
        return {"arr": [rng.randint(-(10**6), 10**6)] * N}
    d = rng.randint(-2000, 2000)
    lo = -(10**6) - min(0, d) * (N - 1)
    hi = 10**6 - max(0, d) * (N - 1)
    start = rng.randint(lo, hi)
    arr = [start + d * i for i in range(N)]
    if shape == "broken":
        i = rng.randrange(1, N - 1)
        arr[i] += 1 if arr[i] < 10**6 else -1
    rng.shuffle(arr)
    return {"arr": arr}
