"""Number of Ways to Divide a Long Corridor at 3 * 10^4 positions with an even number of seats
spread among plants, so a DP that tries every earlier divider for every position costs 4.5 * 10^8
steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    rate = rng.uniform(0.05, 0.3)
    corridor = ["S" if rng.random() < rate else "P" for _ in range(N)]
    if corridor.count("S") % 2:
        corridor[corridor.index("P")] = "S"
    return {"corridor": "".join(corridor)}
