"""Split Array Largest Sum at the maximum n = 1000 and k = 50: ~100 values near 10^6 at one end
(the front for two seeds, the back for one) and small ones after, so every part's best split sits
in the heavy end and even a partition DP that stops scanning once the last part outweighs the
best does ~2.5 * 10^7 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 1000
HEAVY = 100


def generate(rng):
    shape = pick_shape(rng)
    heavy = [rng.randint(5 * 10**5, 10**6) for _ in range(HEAVY)]
    # The light tail sums below any part of the heavy end, so no backward scan stops early.
    light = [rng.randint(0, 1000) for _ in range(N - HEAVY)]
    nums = light + heavy if shape == 2 else heavy + light
    return {"nums": nums, "k": min(50, N)}
