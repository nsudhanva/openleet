"""Minimum Number of Swaps to Make the String Balanced at length 10^5: mostly every ']' before every
'[' (so rescanning after each swap is quadratic) with a block nested 2 * 10^4 deep spliced in (so
repeatedly deleting "[]" pairs is quadratic too)."""

SEEDS = 2
N = 10**5
DEPTH = 2 * 10**4


def generate(rng):
    half = (N - 2 * DEPTH) // 2
    chars = ["]"] * half + ["["] * half
    # Trade a tenth of each half with the other, keeping the counts equal.
    for _ in range(half // 10):
        i, j = rng.randrange(half), rng.randrange(half, 2 * half)
        chars[i], chars[j] = chars[j], chars[i]
    at = rng.randrange(len(chars) + 1)
    chars[at:at] = ["["] * DEPTH + ["]"] * DEPTH
    return {"s": "".join(chars)}
