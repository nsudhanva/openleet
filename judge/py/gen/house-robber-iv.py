"""House Robber IV at n = 10,001 with k near n / 3, so the answer is near the median value and
trying candidate capabilities in order from either end costs ~5 * 10^7 steps."""

SEEDS = 2
N = 10001


def generate(rng):
    nums = [rng.randint(1, 10**9) for _ in range(N)]
    k = min(max(N // 3 + rng.randint(-50, 50), 1), (N + 1) // 2)
    return {"nums": nums, "k": k}
