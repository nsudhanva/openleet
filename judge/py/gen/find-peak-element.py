"""Find Peak Element at n = 1000 with exactly one peak (strictly up, then strictly down), so the
answer is unique; the peak may sit at either end."""

SEEDS = 3
N = 1000


def generate(rng):
    peak = rng.choice([0, N - 1, rng.randrange(N)])
    up = sorted(rng.sample(range(-(2**31), 2**31 - 1), peak + 1))
    down = sorted(rng.sample(range(-(2**31), up[-1]), N - peak - 1), reverse=True)
    return {"nums": up + down}
