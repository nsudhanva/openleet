"""Maximum Frequency After Subarray Operation at n = 5 * 10^4 over values 1-50 where k and one
other value dominate, so trying every pair of that value's occurrences as the subarray ends is
~2.5 * 10^8 steps and counting every subarray's most common value far more."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    k = rng.randint(1, 50)
    top = rng.choice([v for v in range(1, 51) if v != k])
    weights = [1] * 50
    weights[k - 1] = 20
    weights[top - 1] = 60
    return {"nums": rng.choices(range(1, 51), weights, k=N), "k": k}
