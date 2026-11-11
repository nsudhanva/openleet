"""Find the Longest Equal Subarray at n = 10^5: half the values are one or two heavy values and
the rest all distinct, so checking every subarray, every pair of equal values, or restarting a
window per start is quadratic."""

SEEDS = 2
N = 10**5


def generate(rng):
    values = rng.sample(range(1, N + 1), N // 2 + 2)
    heavy, noise = values[: rng.randint(1, 2)], values[2:]
    nums = noise + [rng.choice(heavy) for _ in range(N - len(noise))]
    rng.shuffle(nums)
    return {"nums": nums, "k": rng.randint(N // 20, N // 10)}
