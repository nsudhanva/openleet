"""Find the K-Sum of an Array at n = 2 * 10^4 and k = 2000, with a block of +-1 values among
random ones, so keeping the k largest subset sums while adding each value is ~4 * 10^7 steps
and merging the smallest ones cannot stop after a few values."""

SEEDS = 2
N = 2 * 10**4
K = 2000


def generate(rng):
    # no zeros: a zero makes the k-th smallest subset sum 0 at once
    ones = rng.choice((N // 8, N // 5))
    nums = [rng.choice((-1, 1)) for _ in range(ones)]
    nums += [rng.randint(-(10**9), 10**9) for _ in range(N - ones)]
    rng.shuffle(nums)
    return {"nums": nums, "k": K}
