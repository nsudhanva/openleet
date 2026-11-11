"""Prime In Diagonal on a 200 x 200 matrix whose diagonals hold mostly primes just below 4 * 10^6,
rising in scan order, so trial division by every number below x does ~10^9 divisions where
sqrt(x) bounds suffice."""

from _shapes import primes_upto

SEEDS = 2
N = 200
LIMIT = 4 * 10**6
WINDOW = 10**5


def generate(rng):
    # Primes in (LIMIT - WINDOW, LIMIT], by a segmented sieve.
    lo = LIMIT - WINDOW + 1
    mark = bytearray([1]) * WINDOW
    for p in primes_upto(int(LIMIT**0.5) + 1):
        start = max(p * p, (lo + p - 1) // p * p)
        mark[start - lo :: p] = bytes(len(range(start - lo, WINDOW, p)))
    big = [lo + i for i in range(WINDOW) if mark[i]]
    nums = [[rng.randint(1, LIMIT) for _ in range(N)] for _ in range(N)]
    # Rising primes, so skipping values below the best prime found so far saves nothing.
    diagonal = sorted(rng.sample(big, 2 * N))
    for i in range(N):
        for k, j in enumerate((i, N - 1 - i)):
            prime = diagonal[2 * i + k]
            nums[i][j] = prime if rng.random() < 0.9 else rng.randint(1, prime)
    return {"nums": nums}
