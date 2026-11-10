"""Single-Threaded CPU with 10^5 tasks: all enqueued at once (heap ordering by time then index),
random arrivals with idle gaps, or many equal processing times."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.getrandbits(6) % 3
    if shape == 0:
        tasks = [[1, rng.randint(1, 10**9)] for _ in range(N)]
    elif shape == 1:
        tasks = [[rng.randint(1, 10**9), rng.randint(1, 10**4)] for _ in range(N)]
    else:
        tasks = [[rng.randint(1, 1000), rng.randint(1, 3)] for _ in range(N)]
    return {"tasks": tasks}
