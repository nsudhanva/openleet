"""Subsequence of Size K With the Largest Even Sum with an odd top-k sum and k = n / 2: random
numbers at n = 2 * 10^4 (trying every swap of a chosen and an unchosen number is ~10^8 pairs),
or n = 10^5 with every unchosen number even and every chosen number even but one (a scan of the
unchosen numbers for each chosen one never stops early, ~2.5 * 10^9 steps)."""

from _shapes import pick_shape

SEEDS = 2
N = 2 * 10**4
BIG = 10**5
LIMIT = 10**5


def generate(rng):
    if pick_shape(rng) != 0:
        k = BIG // 2
        rest = [2 * rng.randint(0, LIMIT * 2 // 5 // 2) for _ in range(BIG - k)]
        chosen = [2 * rng.randint(LIMIT * 2 // 5 // 2 + 1, LIMIT // 2) for _ in range(k)]
        chosen[rng.randrange(k)] = 2 * rng.randint(LIMIT * 2 // 5 // 2 + 1, LIMIT // 2 - 1) + 1
        nums = rest + chosen
        rng.shuffle(nums)
        return {"nums": nums, "k": k}
    k = N // 2
    while True:
        nums = [rng.randint(0, LIMIT) for _ in range(N)]
        if sum(sorted(nums)[-k:]) % 2:
            return {"nums": nums, "k": k}
