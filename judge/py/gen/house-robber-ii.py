"""House Robber II at the maximum n = 100 (values up to 1000), with heavy houses at both ends so
the circle matters."""

SEEDS = 2


def generate(rng):
    nums = [rng.randint(0, 1000) for _ in range(100)]
    if rng.random() < 0.5:
        nums[0] = nums[-1] = 1000
    return {"nums": nums}
