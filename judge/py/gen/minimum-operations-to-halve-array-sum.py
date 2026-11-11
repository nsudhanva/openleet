"""Minimum Operations to Halve Array Sum at n = 10^5 with 98% of values in [4.5, 5] * 10^6 and 2%
in [9, 10] * 10^6, so about n halvings are needed (the big values twice) and keeping the order
by a scan or a sorted-list insert each time is quadratic."""

SEEDS = 2
N = 10**5
LIMIT = 10**7


def generate(rng):
    nums = []
    for _ in range(N):
        if rng.random() < 0.02:
            nums.append(rng.randint(LIMIT * 9 // 10, LIMIT))
        else:
            nums.append(rng.randint(LIMIT * 9 // 20, LIMIT // 2))
    return {"nums": nums}
