"""Minimum Speed to Arrive on Time with 1000 roads and under an hour to spare for the last one,
so the answer is ~10^5 to 10^7 and trying speeds 1, 2, 3, ... with an O(n) check each never
finishes against binary search."""

SEEDS = 2
N = 1000
DIST = 10**5


def generate(rng):
    dist = [rng.randint(1, DIST) for _ in range(N)]
    return {"dist": dist, "hour": round(N - 1 + rng.randint(1, 99) / 100, 2)}
