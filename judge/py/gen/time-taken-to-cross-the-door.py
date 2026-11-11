"""Time Taken to Cross the Door at n = 3 * 10^4 with most people arriving in the first few
seconds, so rescanning everyone still waiting each second is ~4 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    early = rng.randint(N * 8 // 10, N)
    arrival = sorted(
        [rng.randint(0, 10) for _ in range(early)] + [rng.randint(0, N) for _ in range(N - early)]
    )
    return {"arrival": arrival, "state": [rng.randint(0, 1) for _ in range(N)]}
