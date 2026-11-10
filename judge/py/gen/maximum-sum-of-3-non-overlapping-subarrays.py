"""Maximum Sum of 3 Non-Overlapping Subarrays at n = 2 * 10^4, k from 1 to n / 3, one seed
with values from a tiny set so many windows tie and the lexicographically smallest wins."""

SEEDS = 3
N = 2 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(1, 2**16 - 1) for _ in range(N)]
    else:
        nums = [rng.randint(1, 2) for _ in range(N)]
    k = rng.choice((1, N // 3, rng.randint(1, N // 3)))
    return {"nums": nums, "k": k}
