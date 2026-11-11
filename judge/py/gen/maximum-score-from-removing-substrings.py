"""Maximum Score from Removing Substrings at length 10^5: one long nested run of the dearer pair
(a^k b^k for "ab") and a shorter one of the other, so removing one pair at a time and rescanning
costs ~5 * 10^9 character moves."""

SEEDS = 2
N = 10**5


def generate(rng):
    x, y = rng.randint(1, 10**4), rng.randint(1, 10**4)
    hi, lo = ("ab", "ba") if x >= y else ("ba", "ab")
    k = rng.randint(N * 2 // 5, N * 9 // 20)
    j = (N - 2 * k - 1) // 2
    s = hi[0] * k + hi[1] * k + rng.choice("xyz") + lo[0] * j + lo[1] * j
    return {"s": s, "x": x, "y": y}
