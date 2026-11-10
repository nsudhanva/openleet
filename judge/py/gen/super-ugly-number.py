"""Super Ugly Number at n = 10^5 with 100 primes, the size where heap-with-duplicates or
O(n * k) scans are slow, and the answer still fits in 32 bits."""

from _shapes import primes_upto

SEEDS = 2
N = 10**5


def generate(rng):
    all_primes = primes_upto(1000)
    if rng.random() < 0.5:
        primes = all_primes[:100]
    else:
        # Keep the small primes so the 10^5-th value stays far below 2^31.
        primes = sorted(all_primes[:40] + rng.sample(all_primes[40:], 60))
    return {"n": rng.choice([N, rng.randint(9 * 10**4, N)]), "primes": primes}
