"""Choose K Elements With Maximum Sum at n = 2 * 10^4 with some repeated nums1 values and k
anywhere up to n, so collecting and ranking the smaller elements afresh for every index is
quadratic."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**6


def generate(rng):
    top = rng.choice((N // 4, LIMIT))
    nums1 = [rng.randint(1, top) for _ in range(N)]
    nums2 = [rng.randint(1, LIMIT) for _ in range(N)]
    return {"nums1": nums1, "nums2": nums2, "k": rng.randint(1, N)}
