"""Greatest Sum Divisible by Three at n = 4 * 10^4 (the maximum) with a total that is not a multiple
of 3, so trying every pair of elements to drop costs ~10^8 pair checks."""

SEEDS = 2
N = 40000


def generate(rng):
    nums = [rng.randint(1, 10**4) for _ in range(N)]
    if sum(nums) % 3 == 0:
        nums[-1] += 1 if nums[-1] < 10**4 else -1
    return {"nums": nums}
