"""Divide Intervals Into Minimum Number of Groups at n = 6 * 10^4 intervals that all contain
5 * 10^5, so every interval needs its own group and assigning each to the first free group by a
scan is ~1.8 * 10^9 steps."""

SEEDS = 2
N = 6 * 10**4
MID = 5 * 10**5


def generate(rng):
    return {"intervals": [[rng.randint(1, MID), rng.randint(MID, 2 * MID)] for _ in range(N)]}
