"""Diet Plan Performance at n = 10^5 with k near n / 2, so re-summing every window is
~2.5 * 10^9 additions; the bounds sit around the average window total."""

SEEDS = 2
N = 10**5


def generate(rng):
    calories = [rng.randint(0, 20000) for _ in range(N)]
    k = rng.randint(N * 2 // 5, N * 3 // 5)
    mid = k * 10000
    lower = mid - rng.randint(0, k * 50)
    upper = mid + rng.randint(0, k * 50)
    return {"calories": calories, "k": k, "lower": lower, "upper": upper}
