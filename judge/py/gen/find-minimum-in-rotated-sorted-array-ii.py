"""Find Minimum in Rotated Sorted Array II at n = 5000 with heavy duplicates: almost all values
equal with the minimum hidden in the middle, the worst case for the binary search."""

SEEDS = 3
N = 5000


def generate(rng):
    if rng.random() < 0.6:
        hi = rng.randint(-4999, 5000)
        nums = [hi] * N
        lo_len = rng.randint(1, 3)
        start = rng.randrange(N - lo_len + 1)
        for i in range(start, start + lo_len):
            nums[i] = hi - 1
        # Sorted then rotated: the block of lower values sits at one position.
        return {"nums": nums}
    nums = sorted(rng.randint(-5000, 5000) for _ in range(N))
    k = rng.randint(1, N)
    return {"nums": nums[-k:] + nums[:-k] if k < N else nums}
