"""Maximum Product of Three Numbers at n = 10^4 over [-1000, 1000], one seed mostly
negative so the two-smallest-times-largest case wins."""

SEEDS = 3
N = 10**4


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(-1000, 1000) for _ in range(N)]
    else:
        nums = [rng.randint(-1000, -1) for _ in range(N - 3)] + [
            rng.randint(0, 50) for _ in range(3)
        ]
        rng.shuffle(nums)
    return {"nums": nums}
