"""Partition Array According to Given Pivot at the maximum 10^5 values: all greater values first,
then all smaller ones, a tenth of each half equal to the pivot, so every stable insertion of a
smaller value shifts ~5 * 10^4 elements."""

SEEDS = 2
N = 10**5
LIMIT = 10**6


def generate(rng):
    pivot = rng.randint(-LIMIT // 2, LIMIT // 2)
    half = N // 2
    nums = [pivot if rng.random() < 0.1 else rng.randint(pivot + 1, LIMIT) for _ in range(half)]
    nums += [
        pivot if rng.random() < 0.1 else rng.randint(-LIMIT, pivot - 1) for _ in range(N - half)
    ]
    nums[rng.randrange(N)] = pivot
    return {"nums": nums, "pivot": pivot}
