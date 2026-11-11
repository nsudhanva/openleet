"""10^4 small values plus a few near 10^6, with the threshold just above the length, so the
answer is ~10^5 or more and trying each divisor in turn costs ~10^9 steps or more."""

SEEDS = 2
N = 10**4


def generate(rng):
    big = rng.randint(2, 5)
    nums = [rng.randint(1, 1000) for _ in range(N - big)]
    nums += [rng.randint(9 * 10**5, 10**6) for _ in range(big)]
    rng.shuffle(nums)
    # Each small value costs 1 from any divisor >= 1000, so the big ones share the slack.
    return {"nums": nums, "threshold": N + rng.randint(0, big * 2)}
