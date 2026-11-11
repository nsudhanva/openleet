"""Meeting Scheduler at the maximum 10^4 shuffled slots each, paired so every overlap is shorter
than the duration except the latest one, so checking every pair of slots costs 10^8 steps."""

SEEDS = 2
N = 10**4
STEP = 10**5


def generate(rng):
    duration = rng.randint(100, STEP // 4)
    slots1, slots2 = [], []
    for i in range(N):
        t = i * STEP + rng.randrange(STEP // 10)
        a = rng.randint(duration + 1, STEP // 3)
        overlap = rng.randint(duration, a) if i == N - 1 else rng.randrange(duration)
        b = rng.randint(max(overlap, 1), STEP // 3)
        slots1.append([t, t + a])
        slots2.append([t + a - overlap, t + a - overlap + b])
    rng.shuffle(slots1)
    rng.shuffle(slots2)
    return {"slots1": slots1, "slots2": slots2, "duration": duration}
