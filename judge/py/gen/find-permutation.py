"""Find Permutation at length 10^5, the maximum, made of a few long runs of 'D', so fixing
descents by adjacent swaps, or inserting at the start of each run, is quadratic."""

SEEDS = 2
N = 10**5


def generate(rng):
    s = ["D"] * N
    for _ in range(rng.randint(1, 4)):
        s[rng.randrange(N)] = "I"
    return {"s": "".join(s)}
