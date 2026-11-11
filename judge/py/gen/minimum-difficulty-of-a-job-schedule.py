"""Minimum Difficulty of a Job Schedule with 60 jobs over d = 10 days: trying every way to cut
the jobs into days without memoization is C(59, 9) ~ 10^10 schedules."""

SEEDS = 2
N = 60
D = 10


def generate(rng):
    return {"jobDifficulty": [rng.randint(0, 1000) for _ in range(N)], "d": D}
