"""K-th Smallest Prime Fraction with arr = 1 plus 999 primes below 3 * 10^4 (about 5 * 10^5
fractions), k anywhere in range."""

SEEDS = 3
N = 1000
LIMIT = 3 * 10**4


def primes():
    sieve = bytearray([1]) * LIMIT
    sieve[0] = sieve[1] = 0
    for i in range(2, int(LIMIT**0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))
    return [i for i in range(LIMIT) if sieve[i]]


def generate(rng):
    arr = [1, *sorted(rng.sample(primes(), N - 1))]
    total = N * (N - 1) // 2
    k = rng.choice([1, total, rng.randint(1, total)])
    return {"arr": arr, "k": k}
