"""Aggregate Two Time Series at 2 * 10^4 points per series with interleaved timestamps (some
shared), so scanning the other series for each timestamp's next value is ~4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    stamps = sorted(rng.sample(range(1, LIMIT + 1), 2 * N - N // 10))
    rng.shuffle(stamps)
    one, two = stamps[:N], stamps[N:]
    two += rng.sample(one, N - len(two))  # shared timestamps
    return {
        "series1": [[t, rng.randint(1, LIMIT)] for t in sorted(one)],
        "series2": [[t, rng.randint(1, LIMIT)] for t in sorted(two)],
    }
