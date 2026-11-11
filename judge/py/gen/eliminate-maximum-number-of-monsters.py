"""Eliminate Maximum Number of Monsters at n = 2 * 10^4 where every monster (or all but the
last) can be shot in time, so simulating minute by minute scans all monsters n times."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    # Monster i must arrive no earlier than minute i + 1: (dist - 1) // speed >= i.
    slack = rng.randint(0, 1)
    times = [i + rng.randint(0, 3) for i in range(N)]
    if slack:
        times[-1] = N - 2  # the last monster arrives one minute too early
    dist, speed = [], []
    for t in times:
        s = rng.randint(1, max(1, (10**5 - 1) // (t + 1)))
        dist.append(t * s + rng.randint(1, s))
        speed.append(s)
    order = list(range(N))
    rng.shuffle(order)
    return {"dist": [dist[i] for i in order], "speed": [speed[i] for i in order]}
