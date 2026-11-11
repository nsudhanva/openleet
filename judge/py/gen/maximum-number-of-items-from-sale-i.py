"""Maximum Number of Items From Sale I with 200 cheap items and budget 1500, so almost every
subset of item types is affordable and enumerating them cannot finish."""

SEEDS = 2
N = 200
BUDGET = 1500


def generate(rng):
    items = [
        [rng.randint(1, 1500 if rng.random() < 0.7 else 30), rng.randint(1, 100)] for _ in range(N)
    ]
    return {"items": items, "budget": BUDGET}
