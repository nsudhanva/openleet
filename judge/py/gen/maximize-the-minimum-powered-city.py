"""Maximize the Minimum Powered City at n = 10^5 with r in [n / 4, n / 3]: station counts fall
steadily along the line, so summing each city's window, or adding each new station's power city by
city in every check of the binary search, is >= 10^9 steps."""

SEEDS = 2
N = 10**5
TOP = 10**5


def generate(rng):
    stations = [
        min(TOP, max(0, TOP - TOP * i // N + rng.randint(-TOP // 100, TOP // 100)))
        for i in range(N)
    ]
    r = rng.randint(N // 4, N // 3)
    return {"stations": stations, "r": r, "k": rng.randint(10**8, 10**9)}
