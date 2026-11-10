"""Minimum Number of K Consecutive Bit Flips at n = 10^5 with k around n / 2, so flipping
each window element by element is ~10^10 steps; inputs are built by flipping windows of an
all-ones array, so they are solvable."""

SEEDS = 3
N = 10**5


def generate(rng):
    k = rng.choice((N // 2, 1000, rng.randint(1, N)))
    if rng.random() < 0.3:
        return {"nums": [rng.randint(0, 1) for _ in range(N)], "k": k}
    diff = [0] * (N + 1)
    for start in range(N - k + 1):
        if rng.random() < 0.3:
            diff[start] ^= 1
            diff[start + k] ^= 1
    nums, flip = [], 0
    for i in range(N):
        flip ^= diff[i]
        nums.append(1 ^ flip)
    return {"nums": nums, "k": k}
