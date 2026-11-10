"""4Sum at the maximum n = 200: large random values with a target that some quadruple hits, or
heavy duplicates in a narrow range with many distinct quadruplets."""

SEEDS = 3
N = 200


def generate(rng):
    if rng.random() < 0.5:
        lim = 25 * 10**7
        nums = [rng.randint(-lim, lim) for _ in range(N)]
        target = sum(rng.sample(nums, 4))
    else:
        nums = [rng.randint(-30, 30) for _ in range(N)]
        target = rng.randint(-20, 20)
    return {"nums": nums, "target": target}
