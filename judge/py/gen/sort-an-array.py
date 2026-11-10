"""Sort an Array at n = 5 * 10^4: random, already sorted, reverse sorted, or all equal (the
quicksort killers)."""

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    shape = rng.getrandbits(4) % 4
    nums = [rng.randint(-5 * 10**4, 5 * 10**4) for _ in range(N)]
    if shape == 1:
        nums.sort()
    elif shape == 2:
        nums.sort(reverse=True)
    elif shape == 3:
        nums = [nums[0]] * N
    return {"nums": nums}
