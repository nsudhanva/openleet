"""Minimum Rounds to Complete All Tasks at n = 5 * 10^4 with each difficulty appearing 2 to 5 times
(~1.4 * 10^4 distinct), so counting each difficulty by a pass over the array is quadratic
against one counter."""

SEEDS = 2
N = 5 * 10**4
LIMIT = 10**9


def generate(rng):
    tasks = []
    while len(tasks) < N:
        tasks += [rng.randint(1, LIMIT)] * min(rng.randint(2, 5), N - len(tasks))
    if tasks.count(tasks[-1]) == 1:
        tasks[-1] = tasks[0]
    rng.shuffle(tasks)
    return {"tasks": tasks}
