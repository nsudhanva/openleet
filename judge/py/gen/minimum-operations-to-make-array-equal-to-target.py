"""Minimum Operations to Make Array Equal to Target at n = 2 * 10^4 where target - nums forms four
long same-sign runs of nearly increasing size, so peeling off each run's minimum and recursing
on the pieces removes one element per pass and is quadratic."""

SEEDS = 2
N = 2 * 10**4
RUNS = 4
LIMIT = 10**8


def generate(rng):
    nums, target = [], []
    size = N // RUNS
    for run in range(RUNS):
        gaps = sorted(rng.randint(1, LIMIT // 2) for _ in range(size))
        for i in range(size - 1):
            if rng.random() < 0.3:
                gaps[i], gaps[i + 1] = gaps[i + 1], gaps[i]
        for gap in gaps:
            low = rng.randint(1, LIMIT - gap)
            if run % 2:
                nums.append(low + gap)
                target.append(low)
            else:
                nums.append(low)
                target.append(low + gap)
    return {"nums": nums, "target": target}
