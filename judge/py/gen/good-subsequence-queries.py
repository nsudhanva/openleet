"""nums and queries of 5 * 10^4 each, the multiples of p covering every multiple of 2p, with an
odd multiple of p added or overwritten now and then so the answer flips often; p is 1, or on one
seed 2 with most queries swapping one non-multiple for another. Recomputing the gcd of the
multiples of p after every query costs ~10^9 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 5 * 10**4
Q = 5 * 10**4
LIMIT = 5 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    p, idle = (2, 0.85) if shape == 2 else (1, 0.0)
    top = LIMIT // p

    def even():  # a multiple of 2p
        return 2 * p * rng.randint(1, top // 2)

    def odd():  # an odd multiple of p: with one present, the gcd of the multiples is p
        return p * (2 * rng.randint(0, (top - 1) // 2) + 1)

    # nums[:m] hold multiples of p, every multiple of 2p at least once; nums[m:] hold odd
    # non-multiples (p = 2 only) that idle queries swap for others, leaving the multiples alone.
    m = N // 2 if idle else N
    nums = [2 * p * j for j in range(1, top // 2 + 1)]
    nums += [even() for _ in range(m - len(nums))]
    rng.shuffle(nums)
    odds = set(rng.sample(range(m), 2))
    for i in odds:
        nums[i] = odd()
    nums += [rng.randrange(1, LIMIT, 2) for _ in range(N - m)]
    queries = []
    for _ in range(Q):
        r = rng.random()
        if r < idle:
            queries.append([rng.randrange(m, N), rng.randrange(1, LIMIT, 2)])
            continue
        r = rng.random()
        if r < 0.002 and odds:
            i = rng.choice(sorted(odds))
            odds.discard(i)
            queries.append([i, even()])
        elif r < 0.003:
            i = rng.randrange(m)
            odds.add(i)
            queries.append([i, odd()])
        else:
            i = rng.randrange(m)
            odds.discard(i)
            queries.append([i, even()])
    return {"nums": nums, "p": p, "queries": queries}
