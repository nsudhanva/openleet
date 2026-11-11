"""Construct the Minimum Bitwise Array II with the maximum 100 primes, nearly all above 10^8
(some ending in long runs of 1 bits) plus 2, so trying every candidate below each prime costs
~10^10 steps."""

SEEDS = 2
N = 100
LOW = 10**8
HIGH = 10**9


def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def prime(rng, ones):
    while True:
        v = rng.randint(LOW, HIGH) | ((1 << ones) - 1)
        if v <= HIGH and is_prime(v):
            return v


def generate(rng):
    nums = [2] + [prime(rng, rng.choice((1, 1, 2, 3, 5, 8, 12))) for _ in range(N - 1)]
    rng.shuffle(nums)
    return {"nums": nums}
