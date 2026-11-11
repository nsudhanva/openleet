"""Find Latest Group of Size m at n = 10^5: the bits are set in ascending (seed 0) or descending
order and m is small, so the answer is step m and walking over the group, or undoing steps from the
end with a sorted list, is ~5 * 10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    m = rng.randint(1, min(100, N))
    arr = list(range(1, N + 1))
    if not rng.randint(0, 1):
        arr.reverse()
    return {"arr": arr, "m": m}
