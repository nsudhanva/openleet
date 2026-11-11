"""Find Minimum Time to Finish All Jobs II at n = 10^5, the maximum, so pairing jobs and
workers by repeated max selection or by insort into sorted lists is quadratic."""

SEEDS = 2
N = 10**5
LIMIT = 10**5


def generate(rng):
    # workers mostly small keeps the JSON under 1 MB
    jobs = [rng.randint(1, rng.choice((LIMIT, 1000))) for _ in range(N)]
    workers = [rng.randint(1, LIMIT if rng.random() < 0.2 else 1000) for _ in range(N)]
    return {"jobs": jobs, "workers": workers}
