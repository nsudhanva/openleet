"""K Radius Subarray Averages at n = 8 * 10^4 with k about n / 4, so summing each window afresh
costs ~1.6 * 10^9 additions even at C speed."""

SEEDS = 2
N = 8 * 10**4


def generate(rng):
    nums = [rng.randint(0, 10**5) for _ in range(N)]
    return {"nums": nums, "k": rng.randint(N // 5, N * 3 // 10)}
