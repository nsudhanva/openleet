"""Task Scheduler II at n = 2 * 10^4 tasks of two or three kinds with space near n, so the answer is
~10^8 days and stepping through the days one at a time is that many steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    kinds = rng.sample(range(1, 10**9 + 1), rng.randint(2, 3))
    return {"tasks": [rng.choice(kinds) for _ in range(N)], "space": rng.randint(N // 2, N)}
