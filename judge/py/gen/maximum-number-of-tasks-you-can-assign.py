"""Maximum Number of Tasks You Can Assign with 2 * 10^4 tasks and workers whose answer lands near
the middle, so checking each count in turn instead of binary searching is quadratic."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    tasks = [rng.randint(0, 10**9) for _ in range(N)]
    workers = [rng.randint(0, 6 * 10**8) for _ in range(N)]
    return {"tasks": tasks, "workers": workers, "pills": N // 10, "strength": 10**8}
