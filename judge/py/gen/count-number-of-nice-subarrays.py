"""Count Number of Nice Subarrays at n = 5 * 10^4: random parities with a mid-sized k, or
sparse odd numbers with k = 1 so nice subarrays are long."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(1, 10**5) for _ in range(N)]
        k = rng.randint(1, 1000)
    else:
        nums = [
            2 * rng.randint(0, 5 * 10**4 - 1) + 1
            if rng.random() < 0.001
            else 2 * rng.randint(1, 5 * 10**4)
            for _ in range(N)
        ]
        k = 1
    return {"nums": nums, "k": k}
