"""Maximum Balanced Subsequence Sum at n = 10^5: random values over the full range, a strictly
decreasing positive sequence, and a mostly rising one with noise. The decreasing one leaves every
element on the DP's frontier of (x - i, best sum) pairs (5 * 10^9 steps to scan it linearly) and
the quadratic DP over every earlier index is 5 * 10^9 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5
LIMIT = 10**9


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    elif shape == 1:
        top = LIMIT - rng.randint(0, 10**6)
        nums = []
        for _ in range(N):
            nums.append(top)
            top -= rng.randint(1, 3000)
    else:
        nums = [10 * i + rng.randint(-5000, 5000) for i in range(N)]
    return {"nums": nums}
