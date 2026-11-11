"""Find Subarray With Bitwise OR Closest to K at n = 2 * 10^4: in two seeds the first and last
values each hold a bit no other value has and k is near 10^9, so no OR reaches k or stops changing
before the end and even an early-exit scan of every subarray is quadratic; in the third, k is one
off the OR of a short interior window, so whole-array prefixes and suffixes miss the answer."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4


def _edges(nums, k):
    """The best difference over single values and whole-array prefixes and suffixes."""
    best = min(abs(x - k) for x in nums)
    for seq in (nums, nums[::-1]):
        acc = 0
        for x in seq:
            acc |= x
            best = min(best, abs(acc - k))
    return best


def generate(rng):
    shape = pick_shape(rng)
    if shape < 2:
        bits = (28, 20)[shape]
        mid = [rng.randint(1, (1 << bits) - 1) for _ in range(N - 2)]
        nums = [1 << bits, *mid, 1 << (bits + 1)]
        return {"nums": nums, "k": rng.randint(9 * 10**8, 10**9)}
    # sparse values (one or two bits) keep short windows' ORs distinct
    nums = [(1 << rng.randrange(28)) | (1 << rng.randrange(28)) for _ in range(N)]
    while True:
        i = rng.randrange(1, N - 4)
        window = 0
        for x in nums[i : i + rng.randint(2, 3)]:
            window |= x
        k = window + rng.choice((-1, 1))
        if _edges(nums, k) > 1:
            return {"nums": nums, "k": k}
