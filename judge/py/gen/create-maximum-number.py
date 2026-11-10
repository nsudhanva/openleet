"""Create Maximum Number with m = n = 500 digits (no leading zeros) and a large k, where
merging needs repeated suffix comparisons over long runs of equal digits."""

SEEDS = 2
L = 500


def digits(rng, few):
    alphabet = [9, 8] if few else list(range(10))
    out = [rng.choice(alphabet) for _ in range(L)]
    if out[0] == 0:
        out[0] = rng.randint(1, 9)
    return out


def generate(rng):
    few = rng.random() < 0.5
    nums1, nums2 = digits(rng, few), digits(rng, few)
    k = rng.randint(L, 2 * L)
    return {"nums1": nums1, "nums2": nums2, "k": k}
