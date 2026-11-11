"""nums1 of 100 and nums2 of 10^5 values with 1000 adds and 1000 counts alternating, so every
count follows a change to nums2 and anything that rescans or recounts nums2 per count costs
~10^8 steps against the intended ~10^5."""

SEEDS = 2
N1 = 100
N2 = 10**5
CALLS = 1000


def generate(rng):
    nums1 = [rng.randint(1, 10**5) for _ in range(N1)]
    nums2 = [rng.randint(1, 10**5) for _ in range(N2)]
    ops, args = ["FindSumPairs"], [[nums1, nums2]]
    for kind in ["add", "count"] * CALLS:
        ops.append(kind)
        if kind == "add":
            args.append([rng.randrange(N2), rng.randint(1, 10**5)])
        else:
            # A sum some pair of the starting arrays makes, so most counts are nonzero.
            args.append([rng.choice(nums1) + rng.choice(nums2)])
    return {"ops": ops, "args": args}
