"""Maximum Number of Distinct Elements After Operations with 3 * 10^4 values in three clusters of
equal values whose range 2k + 1 is just short of the cluster, so probing for a free value from
x - k one at a time is quadratic."""

SEEDS = 2
N = 3 * 10**4
CLUSTERS = 3


def generate(rng):
    size = N // CLUSTERS
    k = size // 2 - rng.randint(1, size // 20 + 1)
    nums = []
    for c in range(CLUSTERS):
        nums += [10**8 * (c + 1) + rng.randint(-5, 5) for _ in range(size)]
    rng.shuffle(nums)
    return {"nums": nums, "k": k}
