"""Minimum Operations to Make Every Element Palindromic with 10^4 values, a third of them odd values
in an even-leading 9-digit block (every palindrome there is even), so stepping by 2 until a
palindrome walks up to ~2.5 * 10^7 steps per value."""

SEEDS = 2
N = 10**4
LIMIT = 10**9


def generate(rng):
    block = LIMIT // 10
    nums = []
    for _ in range(N):
        if rng.random() < 1 / 3:
            lead = rng.choice([2, 4, 6, 8])
            nums.append((lead * block + rng.randrange(block)) | 1)
        else:
            nums.append(rng.randint(1, LIMIT))
    return {"nums": nums}
