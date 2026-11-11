"""Ways to Make a Fair Array at 5 * 10^4 numbers, nearly all 1s with the even and odd sums
balanced so some removals are fair, and re-summing the array per removal is ~2.5 * 10^9 steps."""

SEEDS = 2
N = 5 * 10**4
TOP = 10**4


def generate(rng):
    nums = [1 if rng.random() < 0.95 else rng.randint(1, TOP) for _ in range(N)]
    gap = sum(nums[::2]) - sum(nums[1::2])
    while gap:
        # Raise an odd index when the even sum is ahead, an even one otherwise.
        i = rng.randrange(1 if gap > 0 else 0, N, 2)
        step = min(abs(gap), TOP - nums[i])
        nums[i] += step
        gap += -step if gap > 0 else step
    return {"nums": nums}
