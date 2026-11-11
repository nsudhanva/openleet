"""Maximum Coin Collection at n = 10^4 over the full value range, so running the lane DP from
every entry mile is ~10^8 state updates."""

SEEDS = 2
N = 10**4
LIMIT = 10**9


def generate(rng):
    return {
        "lane1": [rng.randint(-LIMIT, LIMIT) for _ in range(N)],
        "lane2": [rng.randint(-LIMIT, LIMIT) for _ in range(N)],
    }
