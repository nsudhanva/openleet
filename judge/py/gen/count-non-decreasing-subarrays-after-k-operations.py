"""Count Non-Decreasing Subarrays After K Operations at n = 2 * 10^4: flat noise or an upward
trend with noise, k sized for windows of thousands, so extending every start until the cost
passes k costs ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(1, 100) for _ in range(N)]
        k = rng.randint(50 * N // 10, 50 * N // 4)
    else:
        nums = [1 + i * 4 * 10**4 + rng.randrange(10**5) for i in range(N)]
        k = rng.randint(10**7, 3 * 10**7)
    return {"nums": nums, "k": k}
