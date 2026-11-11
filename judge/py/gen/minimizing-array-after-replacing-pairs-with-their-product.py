"""Minimizing Array After Replacing Pairs With Their Product at n = 10^5: 1s and 2s that merge,
then large values that never do, so each in-place merge shifts the long tail and restarting the
scan after each merge is quadratic."""

SEEDS = 2
N = 10**5
LIMIT = 10**9
BIG = 10**5


def generate(rng):
    small = [rng.randint(1, 2) for _ in range(N // 2)]
    big = [rng.randint(BIG, LIMIT) for _ in range(N - N // 2)]
    return {"nums": small + big, "k": LIMIT}
