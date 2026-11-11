"""Stone Game VIII at n = 2 * 10^4, so trying every move from every position is ~2 * 10^8
steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**4


def generate(rng):
    return {"stones": [rng.randint(-LIMIT, LIMIT) for _ in range(N)]}
