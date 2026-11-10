"""Task Scheduler at 10^4 tasks: one dominant letter with a large cooldown (idle-heavy), all
26 letters evenly (no idle), or random, punishing step-by-step simulation."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        tasks = ["A"] * 5000 + [rng.choice(UPPER[1:]) for _ in range(N - 5000)]
        n = 100
    elif shape == 1:
        tasks = [UPPER[i % 26] for i in range(N)]
        n = rng.randint(0, 30)
    else:
        tasks = [rng.choice(UPPER) for _ in range(N)]
        n = rng.randint(0, 100)
    rng.shuffle(tasks)
    return {"tasks": tasks, "n": n}
