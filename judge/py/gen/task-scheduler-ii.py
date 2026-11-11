"""Task Scheduler II at n = 2 * 10^4: two or three kinds with space near n, so the answer is ~10^8
days and stepping through the days one at a time is that many steps; or tasks that repeat only
about 10^4 positions apart, so looking back for the previous equal task is ~10^8 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        kinds = rng.sample(range(1, 10**9 + 1), rng.randint(2, 3))
        tasks = [rng.choice(kinds) for _ in range(N)]
    else:
        kinds = rng.sample(range(1, 10**9 + 1), N // 2)
        tasks = [rng.choice(kinds) for _ in range(N)] if shape == 1 else kinds + kinds
    return {"tasks": tasks, "space": rng.randint(N // 2, N)}
