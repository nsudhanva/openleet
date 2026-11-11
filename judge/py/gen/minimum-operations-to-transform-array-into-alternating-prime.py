"""Minimum Operations to Transform Array into Alternating Prime at n = 10^5 (the limit) with large
primes at the odd indices and values just past a prime at the even ones, so testing each
candidate by trial division costs ~3 * 10^7 divisions against a sieve."""

SEEDS = 2
N = 10**5
LIMIT = 10**5


def generate(rng):
    sieve = [True] * (LIMIT + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(LIMIT**0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = [False] * len(range(i * i, LIMIT + 1, i))
    primes = [p for p in range(LIMIT // 2, LIMIT + 1) if sieve[p]]
    nums = []
    for i in range(N):
        p = rng.choice(primes)
        nums.append(p if i % 2 else min(p + 1, LIMIT))
    return {"nums": nums}
