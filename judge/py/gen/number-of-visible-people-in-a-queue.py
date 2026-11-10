"""Visible People at n = 10^5 with unique heights: random, or descending so every person sees
only the next one but a naive scan walks the whole suffix."""

SEEDS = 2
N = 10**5


def generate(rng):
    heights = rng.sample(range(1, 10**5 + 1), N)
    if rng.random() < 0.5:
        heights.sort(reverse=True)
        # Keep a few random swaps so it is not perfectly monotone.
        for _ in range(100):
            i = rng.randrange(N - 1)
            heights[i], heights[i + 1] = heights[i + 1], heights[i]
    return {"heights": heights}
