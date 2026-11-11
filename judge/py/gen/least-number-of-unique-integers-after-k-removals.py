"""Least Number of Unique Integers after K Removals at n = 2 * 10^4 with ~10^4 distinct values and
k = n / 2, so removing one element at a time from the rarest value costs ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    arr = []
    while len(arr) < N:
        v = rng.randint(1, 10**9)
        arr += [v] * min(rng.randint(1, 3), N - len(arr))
    rng.shuffle(arr)
    return {"arr": arr, "k": N // 2 + rng.randint(-N // 200, N // 200)}
