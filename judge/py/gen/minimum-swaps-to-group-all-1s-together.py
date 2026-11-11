"""Minimum Swaps to Group All 1's Together at n = 10^5 with half the entries 1, so re-counting
every window of length k = 5 * 10^4 is ~2.5 * 10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    data = [1] * (N // 2) + [0] * (N - N // 2)
    rng.shuffle(data)
    return {"data": data}
