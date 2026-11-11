"""Split Array with Equal Sum at n = 2,000, always false. Zeros (or x, -x repeated) and then one
large last element give most (i, j) pairs equal first two parts, so a triple loop does ~10^9
steps; a large first and last element around zeros give ~n^2 / 2 pairs of equal outer parts and no
valid middle, so fixing the outer cuts first and then scanning the middle does ~n^3 / 6 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 2000
LIMIT = 10**6


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        body = [0] * (N - 1)
    elif shape == 1:
        # Prefix sums alternate 0, x, so half the (i, j) pairs have equal first two parts.
        x = rng.randint(1, LIMIT // 10)
        body = [x if i % 2 == 0 else -x for i in range(N - 1)]
    else:
        ends = rng.randint(LIMIT // 2, LIMIT)
        return {"nums": [ends, *[0] * (N - 2), ends]}
    return {"nums": [*body, rng.randint(LIMIT // 2, LIMIT)]}
