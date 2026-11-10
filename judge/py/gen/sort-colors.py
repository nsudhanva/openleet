"""Sort Colors at n = 300: random, or reverse sorted (all 2s, then 1s, then 0s)."""

SEEDS = 2


def generate(rng):
    nums = [rng.randint(0, 2) for _ in range(300)]
    if rng.random() < 0.5:
        nums.sort(reverse=True)
    return {"nums": nums}
