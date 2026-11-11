"""10^5 distinct values with the maximum last and k either near 10^9 or just under n, so playing
the rounds out takes 10^9 rounds, or 10^5 rounds that each shift the whole array."""

SEEDS = 2
N = 10**5


def generate(rng):
    arr = rng.sample(range(1, 10**6), N - 1)
    arr.append(10**6)
    k = rng.randint(9 * 10**8, 10**9) if rng.getrandbits(1) else N - rng.randint(1, 100)
    return {"arr": arr, "k": k}
