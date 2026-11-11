"""Maximum Tastiness of Candy Basket at n = 2 * 10^4 with small k, so the answer is ~10^7 and
trying every tastiness in turn costs ~10^11 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    return {"price": [rng.randint(1, LIMIT) for _ in range(N)], "k": rng.randint(2, min(100, N))}
