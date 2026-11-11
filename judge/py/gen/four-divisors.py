"""3000 values below 10^5, each a prime near the top or a product of two distinct primes, so
every value has at most four divisors and testing every candidate divisor up to the value costs
~1.5 * 10^8 steps."""

from bisect import bisect_right

from _shapes import primes_upto

SEEDS = 2
N = 3000
LIMIT = 10**5


def generate(rng):
    primes = primes_upto(LIMIT)
    small = primes[: bisect_right(primes, int(LIMIT**0.5))]
    nums = []
    for _ in range(N):
        if rng.getrandbits(1):
            nums.append(rng.choice(primes[-5000:]))
        else:
            # p * q with p < q <= LIMIT / p: exactly four divisors.
            p = rng.choice(small)
            lo, hi = bisect_right(primes, p), bisect_right(primes, LIMIT // p)
            nums.append(p * primes[rng.randrange(lo, hi)])
    return {"nums": nums}
