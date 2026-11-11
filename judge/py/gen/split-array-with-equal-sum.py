"""Split Array with Equal Sum at n = 2,000: zeros (or x, -x repeated) and then one large last
element that breaks every split, so most (i, j) pairs have equal first two parts and a triple
loop does ~10^9 steps, while the answer is false."""

SEEDS = 2
N = 2000
LIMIT = 10**6


def generate(rng):
    if rng.random() < 0.5:
        body = [0] * (N - 1)
    else:
        # Prefix sums alternate 0, x, so half the (i, j) pairs have equal first two parts.
        x = rng.randint(1, LIMIT // 10)
        body = [x if i % 2 == 0 else -x for i in range(N - 1)]
    return {"nums": [*body, rng.randint(LIMIT // 2, LIMIT)]}
