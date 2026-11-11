"""Unit Conversion I at 2 * 10^4 units joined in one chain from unit 0 under random labels, so
walking from unit 0 to each unit separately is ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    order = [0, *rng.sample(range(1, N), N - 1)]
    conversions = [[order[i - 1], order[i], rng.randint(1, 10**9)] for i in range(1, N)]
    rng.shuffle(conversions)
    return {"conversions": conversions}
