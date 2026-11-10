"""Sliding Window Maximum at n = 10^5 with large k: strictly decreasing values (the deque
never pops), increasing values, or random, so O(n * k) does ~2.5 * 10^9 work."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.getrandbits(6) % 3
    if shape == 0:
        nums = sorted((rng.randint(-(10**4), 10**4) for _ in range(N)), reverse=True)
    elif shape == 1:
        nums = sorted(rng.randint(-(10**4), 10**4) for _ in range(N))
    else:
        nums = [rng.randint(-(10**4), 10**4) for _ in range(N)]
    k = rng.choice([N // 2, rng.randint(1, N), N, 1])
    return {"nums": nums, "k": k}
