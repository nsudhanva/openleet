"""Increasing Triplet at n = 5 * 10^5: strictly decreasing (false), decreasing with the only
triplet at the very end, or a zigzag that keeps resetting the candidates."""

SEEDS = 3
N = 5 * 10**5


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        start = rng.randint(0, 10**5)
        nums = list(range(start, start - N, -1))
    elif shape == 1:
        start = rng.randint(0, 10**5)
        nums = list(range(start, start - N, -1))
        nums[-3:] = [start - N - 5, start - N - 4, rng.choice([start - N - 3, start - N - 6])]
    else:
        nums = []
        v = 4 * 10**5
        while len(nums) < N:
            nums.extend([v, v + 1])
            v -= 2
        nums = nums[:N]
    return {"nums": nums}
