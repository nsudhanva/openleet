"""4Sum II at the maximum n = 200: narrow values give huge counts, wide values give few
matches; both make an n^4 scan do 1.6 * 10^9 steps."""

SEEDS = 2
N = 200


def generate(rng):
    lim = rng.choice([50, 2**28])
    return {f"nums{i}": [rng.randint(-lim, lim) for _ in range(N)] for i in range(1, 5)}
