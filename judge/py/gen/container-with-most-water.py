"""Container With Most Water at n = 10^5: random heights, or a mountain (rising then falling)
where the best pair is far from the ends of a greedy scan."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        height = [rng.randint(0, 10**4) for _ in range(N)]
    else:
        half = N // 2
        up = sorted(rng.randint(0, 10**4) for _ in range(half))
        down = sorted((rng.randint(0, 10**4) for _ in range(N - half)), reverse=True)
        height = up + down
    return {"height": height}
