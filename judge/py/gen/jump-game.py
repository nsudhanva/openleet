"""Jump Game at n = 10^4: a countdown that dies on a zero just before the end (false), big jumps
that clear every zero (true), or random small jumps."""

SEEDS = 3
N = 10**4


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        nums = [N - 1 - i for i in range(N - 1)] + [0]
        nums = [max(0, v - 1) for v in nums]  # each index reaches exactly the zero at N - 2
        nums[-1] = rng.randint(0, 10**5)
    elif shape == 1:
        nums = [rng.choice([0, 0, 0, rng.randint(1, 10**5)]) for _ in range(N)]
        nums[0] = max(nums[0], 1)
    else:
        nums = [rng.randint(0, 3) for _ in range(N)]
    return {"nums": nums}
