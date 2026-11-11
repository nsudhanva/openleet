"""Reduce Array Size to The Half at n = 3 * 10^4 with ~10^4 distinct values of skewed frequency,
so counting each value by a scan costs ~3 * 10^8 comparisons."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    values = rng.sample(range(1, 10**5 + 1), N // 3)
    arr = [
        values[min(int(rng.expovariate(1 / len(values) * 4)), len(values) - 1)] for _ in range(N)
    ]
    rng.shuffle(arr)
    return {"arr": arr}
