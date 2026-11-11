"""Maximum Gap Between Stations with 2 * 10^4 stations over 'abc' and a random subsequence of
half of them as the workers, so redoing the greedy prefix and suffix matches for every worker is
~4 * 10^8 steps."""

SEEDS = 2
M = 2 * 10**4


def generate(rng):
    station = "".join(rng.choice("abc") for _ in range(M))
    picks = sorted(rng.sample(range(M), rng.randint(M // 3, M // 2)))
    return {"skill": "".join(station[i] for i in picks), "station": station}
