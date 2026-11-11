"""Count Subarrays Where Max Element Appears at Least K Times at n = 2 * 10^4 with the maximum
spread thinly and k half its count, so extending each start until k copies costs ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**6


def generate(rng):
    nums = [rng.randint(1, LIMIT - 1) for _ in range(N)]
    spots = rng.sample(range(N), N // 10)
    for i in spots:
        nums[i] = LIMIT
    return {"nums": nums, "k": len(spots) // 2}
