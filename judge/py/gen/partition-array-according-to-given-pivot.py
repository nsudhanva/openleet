"""Partition Array According to Given Pivot at the maximum 10^5 values: a third greater than the
pivot, then a third equal to it, then a third smaller, so every stable insertion into one list
shifts up to ~6 * 10^4 elements (~1.6 s a seed against ~0.05 s for the reference), and 10 seeds
put that past the time limit."""

SEEDS = 10
N = 10**5
LIMIT = 10**6


def generate(rng):
    pivot = rng.randint(-LIMIT // 2, LIMIT // 2)
    third = N // 3
    nums = [rng.randint(pivot + 1, LIMIT) for _ in range(third)]
    nums += [pivot] * third
    nums += [rng.randint(-LIMIT, pivot - 1) for _ in range(N - 2 * third)]
    return {"nums": nums, "pivot": pivot}
