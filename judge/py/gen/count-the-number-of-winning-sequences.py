"""Count the Number of Winning Sequences at n = 600 random moves, so a DP that tracks Alice's and
Bob's scores separately (~n^3 / 2 states) instead of their difference does ~10^8 steps."""

SEEDS = 2
N = 600


def generate(rng):
    return {"s": "".join(rng.choice("FWE") for _ in range(N))}
