"""Number of Different Subsequences GCDs at n = 10^5 distinct values, either a permutation of
1..10^5 or a sample of 10^5 from 1..2 * 10^5, so the harmonic sieve stops at once for most
candidates (~3 * 10^5 steps) while taking the GCD of each candidate's multiples by a scan of nums
is ~10^10 steps."""

from _shapes import pick_shape

SEEDS = 2
N = 10**5
TOPS = (10**5, 2 * 10**5)


def generate(rng):
    top = TOPS[pick_shape(rng) % 2]
    return {"nums": rng.sample(range(1, top + 1), N)}
