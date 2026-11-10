"""3Sum at n = 3000: wide random values, or heavy duplicates in a narrow range so there are
many distinct triplets and duplicate-skipping matters."""

SEEDS = 3
N = 3000


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(-(10**5), 10**5) for _ in range(N)]
    else:
        width = rng.choice([150, 600])
        nums = [rng.randint(-width, width) for _ in range(N)]
        nums[rng.randrange(N)] = 0
    return {"nums": nums}
