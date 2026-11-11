"""Split Array With Minimum Difference at n = 5 * 10^4: a strictly increasing run up to a peak
(or a two-value plateau) and a strictly decreasing run after it, so checking each split by
rescanning both sides is ~10^9 steps."""

SEEDS = 2
N = 5 * 10**4
LIMIT = 10**5


def generate(rng):
    # The first draw picks the shape, so seeds 0 and 1 take different branches.
    plateau = rng.random() < 0.5
    peak = rng.randint(N // 3, 2 * N // 3)
    up = sorted(rng.sample(range(1, LIMIT // 2), peak))
    down = sorted(rng.sample(range(1, LIMIT // 2), N - peak), reverse=True)
    top = LIMIT - rng.randrange(100)
    if plateau:
        return {"nums": [*up[:-1], top, top, *down[1:]]}
    return {"nums": [*up, top, *down[1:]]}
