"""Filling Bookcase Shelves at the maximum 1000 books, all of thickness 1 on a shelf 1000 wide, so
every earlier book can share the last shelf: the DP tries ~5 * 10^5 splits and recomputing each
shelf's height from scratch is ~1.7 * 10^8 steps."""

SEEDS = 2
N = 1000


def generate(rng):
    return {"books": [[1, rng.randint(1, 1000)] for _ in range(N)], "shelfWidth": 1000}
