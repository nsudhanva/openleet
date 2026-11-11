"""Make K-Subarray Sums Equal at n = 10^4 with gcd(n, k) of 1 or 2, so one or two cycles hold
every element and trying each element as the common value is ~10^8 steps."""

from math import gcd

SEEDS = 2
N = 10**4


def generate(rng):
    want = 1 + rng.randrange(2)
    while True:
        k = rng.randint(1, N)
        if gcd(N, k) == want:
            break
    arr = [rng.randint(1, 10**9) for _ in range(N)]
    return {"arr": arr, "k": k}
