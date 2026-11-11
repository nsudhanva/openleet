"""Super Ugly Number with answers of 4 * 10^7 to 2 * 10^9: n up to 10^4 over the 100 largest
primes below 1000, or a handful of small primes with n near the last value under 2^31, so
testing every integer up to the answer is hopeless."""

from heapq import heappop, heappush

from _shapes import primes_upto

SEEDS = 2
N = 10**4
LIMIT = 2**31 - 1


def count_upto(primes, limit):
    """How many super ugly numbers are at most limit."""
    heap, seen, count = [1], {1}, 0
    while heap:
        x = heappop(heap)
        count += 1
        for p in primes:
            if x * p <= limit and x * p not in seen:
                seen.add(x * p)
                heappush(heap, x * p)
    return count


def generate(rng):
    small = primes_upto(1000)
    if rng.random() < 0.5:
        # Primes from 347 up: 5151 values below 10^6, then products of three from 4 * 10^7.
        return {"n": rng.randint(6000, N), "primes": small[-100:]}
    primes = sorted(rng.sample(small[:10], rng.randint(4, 5)))
    total = count_upto(primes, LIMIT)
    return {"n": total - rng.randint(0, total // 20), "primes": primes}
