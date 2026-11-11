"""Maximum Size of a Set After Removals at the maximum n = 2 * 10^4: one array has ~0.8n values of
its own, past its n / 2 cap, the other ~0.3n, plus ~0.1n shared and repeats, so the answer is
below n and deduplicating and intersecting by list scans costs ~4 * 10^8 comparisons."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    # The first draw is 0.84 for seed 0 and 0.13 for seed 1, so the big side differs.
    swap = rng.random() < 0.5
    own_big = rng.randint(3 * N // 4, 17 * N // 20)
    shared = rng.randint(N // 10, 3 * N // 20)
    own_small = rng.randint(N // 4, 3 * N // 10)
    pool = rng.sample(range(1, 10**9 + 1), own_big + shared + own_small)
    common = pool[:shared]
    big = pool[shared : shared + own_big] + common
    small = pool[shared + own_big :] + common
    big += [rng.choice(big) for _ in range(N - len(big))]
    small += [rng.choice(small) for _ in range(N - len(small))]
    rng.shuffle(big)
    rng.shuffle(small)
    nums1, nums2 = (small, big) if swap else (big, small)
    return {"nums1": nums1, "nums2": nums2}
