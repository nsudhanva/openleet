"""Minimum Jumps via Prime Teleportation at n = 10^5: many copies of small primes and their
multiples (teleport edges are quadratic if listed one by one), distinct large primes with no
multiples, or random values."""

SEEDS = 3
N = 10**5
TOP = 10**6


def primes_upto(limit):
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            sieve[p * p :: p] = bytearray(len(range(p * p, limit + 1, p)))
    return [i for i in range(limit + 1) if sieve[i]]


def generate(rng):
    kind = rng.choice(("small", "large", "random"))
    if kind == "small":
        nums = [rng.choice((2, 3, 5, 7)) * rng.randint(1, 1000) for _ in range(N)]
    elif kind == "large":
        primes = primes_upto(TOP)
        nums = rng.sample(primes[len(primes) // 2 :], N // 4)
        nums += [rng.choice((1, 4, 9, 25)) for _ in range(N - len(nums))]
        rng.shuffle(nums)
    else:
        nums = [rng.randint(1, TOP) for _ in range(N)]
    return {"nums": nums}
