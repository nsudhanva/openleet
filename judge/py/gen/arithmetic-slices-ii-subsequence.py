"""Arithmetic Slices II at n = 1000: one long non-constant progression (millions of
subsequences, every pair of indices extends many), or narrow random values; both keep the answer
inside 32 bits as the statement guarantees."""

SEEDS = 3
N = 1000
LO, HI = -(2**31), 2**31 - 1


def generate(rng):
    shape = rng.choice(["progression", "narrow", "wide"])
    if shape == "progression":
        d = rng.choice([1, -1, rng.randint(1, 4 * 10**6), -rng.randint(1, 4 * 10**6)])
        start = rng.randint(LO + max(0, -d) * (N - 1), HI - max(0, d) * (N - 1))
        nums = [start + d * i for i in range(N)]
    elif shape == "narrow":
        nums = [rng.randint(-100, 100) for _ in range(N)]
    else:
        nums = [rng.randint(LO, HI) for _ in range(N)]
    return {"nums": nums}
