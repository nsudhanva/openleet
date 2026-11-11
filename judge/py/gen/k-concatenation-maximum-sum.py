"""K-Concatenation Maximum Sum at n = 10^4 and k = 5000, with a positive or a negative total, so
running Kadane over all k copies costs 5 * 10^7 steps."""

SEEDS = 2
N = 10**4
K = 5000


def generate(rng):
    shift = rng.choice([-300, 300])
    arr = [max(-(10**4), min(10**4, rng.randint(-(10**4), 10**4) + shift)) for _ in range(N)]
    return {"arr": arr, "k": K}
