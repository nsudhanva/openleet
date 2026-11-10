"""K-th Smallest Prime Fraction with arr = 1 plus 999 primes below 3 * 10^4 (about 5 * 10^5
fractions), k anywhere in range."""

from _shapes import primes_upto

SEEDS = 3
N = 1000
LIMIT = 3 * 10**4


def generate(rng):
    arr = [1, *sorted(rng.sample(primes_upto(LIMIT - 1), N - 1))]
    total = N * (N - 1) // 2
    k = rng.choice([1, total, rng.randint(1, total)])
    return {"arr": arr, "k": k}
