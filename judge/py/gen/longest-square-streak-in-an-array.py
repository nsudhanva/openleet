"""Longest Square Streak in an Array at n = 5 * 10^4 random values, most without their square in
the array, so searching the list for each square costs ~2.5 * 10^9 comparisons."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    nums = [rng.randint(2, 10**5) for _ in range(N)]
    # One planted streak 2 -> 4 -> 16 -> 256 -> 65536 or 3 -> 9 -> 81 -> 6561.
    x = rng.choice((2, 3))
    while x <= 10**5:
        nums[rng.randrange(N)] = x
        x *= x
    return {"nums": nums}
