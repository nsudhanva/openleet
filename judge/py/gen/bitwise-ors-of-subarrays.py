"""Bitwise ORs of Subarrays at n = 5 * 10^4: random 30-bit values, single-bit powers of two that
make the set of ORs per end position as large as possible, or many zeros."""

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    shape = rng.choice(["random", "powers", "sparse"])
    if shape == "random":
        arr = [rng.randint(0, 10**9) for _ in range(N)]
    elif shape == "powers":
        arr = [1 << rng.randrange(30) for _ in range(N)]
    else:
        arr = [rng.randint(0, 10**9) if rng.random() < 0.01 else 0 for _ in range(N)]
    return {"arr": arr}
