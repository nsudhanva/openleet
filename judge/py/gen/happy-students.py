"""Happy Students at n = 10^4, so checking every group size against every student costs 10^8
steps; values cluster in bands so several group sizes are valid."""

SEEDS = 2
N = 10**4


def generate(rng):
    # A few cut points k where no student has nums == k; each band of values sits strictly
    # between consecutive cuts and holds exactly the students that make the next cut valid.
    cuts = sorted(2 * c for c in rng.sample(range(1, N // 2 - 1), rng.randint(3, 8)))
    nums = []
    lo = 0
    for k in [*cuts, N]:
        nums += [rng.randint(lo, k - 1) for _ in range(k - len(nums))]
        lo = k + 1
    nums = nums[:N]
    rng.shuffle(nums)
    return {"nums": nums}
