"""Number of Zero-Filled Subarrays at 5 * 10^4 values in runs of zeros 6,000 to 20,000 long, so
extending a subarray from every position costs ~4 * 10^8 steps."""

SEEDS = 2
N = 5 * 10**4
LONG = 2 * 10**4
TOP = 10**9


def generate(rng):
    nums = []
    while len(nums) < N:
        nums += [0] * rng.randint(LONG * 3 // 10, LONG)
        nums += [rng.choice((-1, 1)) * rng.randint(1, TOP) for _ in range(rng.randint(1, 3))]
    return {"nums": nums[:N]}
