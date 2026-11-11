"""Check If Array Pairs Are Divisible by k at n = 2 * 10^4 and k = 10^5: the first half has
distinct remainders and their partners sit shuffled in the second half, so pairing each value by
scanning for a partner is quadratic; one of the three seeds breaks a single pair."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4
K = 10**5
LIMIT = 10**9


def value(rng, r):
    """A value in [-LIMIT, LIMIT] that leaves remainder r mod K."""
    return r + K * rng.randint(-LIMIT // K, (LIMIT - r) // K)


def generate(rng):
    broken = pick_shape(rng) == 2
    rems = rng.sample(range(1, (K + 1) // 2), N // 2)
    first = [value(rng, r) for r in rems]
    second = [value(rng, K - r) for r in rems]
    rng.shuffle(second)
    arr = first + second
    if broken:
        i = rng.randrange(N // 2, N)
        arr[i] = value(rng, (arr[i] + rng.randint(1, K - 1)) % K)
    return {"arr": arr, "k": K}
