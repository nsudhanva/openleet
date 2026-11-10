"""Global and Local Inversions on a permutation of 10^5: only adjacent swaps (ideal), or the same
with one swap two apart hidden inside."""

SEEDS = 3
N = 10**5


def generate(rng):
    nums = list(range(N))
    i = 0
    while i < N - 1:
        if rng.random() < 0.5:
            nums[i], nums[i + 1] = nums[i + 1], nums[i]
            i += 2
        else:
            i += 1
    if rng.random() < 0.67:
        j = rng.randrange(N - 2)
        nums[j], nums[j + 2] = nums[j + 2], nums[j]
    return {"nums": nums}
