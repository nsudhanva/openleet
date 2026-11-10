"""Partition into Disjoint Intervals at n = 10^5, built so the only valid splits begin near
the end: the largest left value sits first and the smallest sits at the cut."""

SEEDS = 2
N = 10**5


def generate(rng):
    left_len = rng.choice([rng.randint(N // 2, N - 1), N - 1])
    mid = rng.randint(10**5, 9 * 10**5)
    left = [rng.randint(1, mid) for _ in range(left_len)]
    left[0] = mid
    left[-1] = 0
    right = [rng.randint(mid, 10**6) for _ in range(N - left_len)]
    return {"nums": left + right}
