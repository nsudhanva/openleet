"""Find Minimum Time to Finish All Jobs II at n = 10^5, the maximum, in random order or in
descending order (each insertion into a sorted list lands at the front), so pairing jobs and
workers by repeated max selection or by insort into sorted lists is quadratic."""

from _shapes import pick_shape

SEEDS = 2
N = 10**5
LIMIT = 10**5


def generate(rng):
    # workers mostly small keeps the JSON under 1 MB
    descending = pick_shape(rng) == 1
    jobs = [rng.randint(1, rng.choice((LIMIT, 1000))) for _ in range(N)]
    workers = [rng.randint(1, LIMIT if rng.random() < 0.2 else 1000) for _ in range(N)]
    if descending:
        jobs.sort(reverse=True)
        workers.sort(reverse=True)
    return {"jobs": jobs, "workers": workers}
