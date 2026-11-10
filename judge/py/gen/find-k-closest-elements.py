"""Find K Closest Elements on 10^4 sorted values with many duplicates, x anywhere (including
outside the array), and k up to n."""

SEEDS = 3
N = 10**4


def generate(rng):
    spread = rng.choice([50, 10**4])
    arr = sorted(rng.randint(-spread, spread) for _ in range(N))
    k = rng.choice([1, rng.randint(1, N), N // 2])
    x = rng.randint(-(10**4), 10**4)
    return {"arr": arr, "k": k, "x": x}
