"""Count Subarrays With Majority Element I at n = 1000, where target fills about half the
array so many subarrays are borderline majorities (punishes cubic counting)."""

SEEDS = 2
N = 1000


def generate(rng):
    target = rng.randint(1, 10**9)
    p = rng.choice([0.5, 0.3])
    others = [rng.randint(1, 10**9) for _ in range(5)]
    nums = [target if rng.random() < p else rng.choice(others) for _ in range(N)]
    return {"nums": nums, "target": target}
