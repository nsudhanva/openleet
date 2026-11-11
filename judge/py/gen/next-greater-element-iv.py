"""Next Greater Element IV: two seeds of n = 2 * 10^4 non-increasing values (with runs of equal
values and 20 random ones at the end), so most answers are -1 and a scan to the right for each
index is ~2 * 10^8 steps; one seed of 3 * 10^4 nested (low, high) pairs, where every low has a
first greater element next to it and no second one, so finding the first greater by a stack and
then scanning on for the second is ~4.5 * 10^8 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4
TAIL = 20
PAIRS = 3 * 10**4


def generate(rng):
    if pick_shape(rng) == 1:
        # Each pair (low, low + 1) lies below the previous pair's low, so only the pair's own
        # high exceeds its low.
        nums, low = [], 10**9
        for _ in range(PAIRS):
            gap = rng.randint(2, 12)
            low -= gap
            nums += [low, low + rng.randint(1, gap - 1)]
        return {"nums": nums}
    nums = sorted((rng.randint(0, 10**9) for _ in range(N - TAIL)), reverse=True)
    for i in range(0, N - TAIL - 10, 50):
        nums[i + 1 : i + 10] = [nums[i]] * 9
    nums += [rng.randint(0, 10**9) for _ in range(TAIL)]
    return {"nums": nums}
