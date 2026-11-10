"""Minimum Cost to Hire K Workers at n = 10^4 with k around n / 2, so trying every captain
and sorting the rest is ~10^8 log n."""

SEEDS = 3
N = 10**4


def generate(rng):
    quality = [rng.randint(1, 10**4) for _ in range(N)]
    wage = [rng.randint(1, 10**4) for _ in range(N)]
    return {"quality": quality, "wage": wage, "k": rng.choice((N // 2, N, rng.randint(1, N)))}
