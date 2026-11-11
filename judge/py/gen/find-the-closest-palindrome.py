"""Find the Closest Palindrome for an 18- or 17-digit n whose nearest palindrome is at least
3 * 10^7 away, so stepping outward one number at a time takes tens of millions of checks."""

SEEDS = 2
GAP = 3 * 10**7


def mirror(left, length):
    s = str(left)
    return int(s + s[: length // 2][::-1])


def generate(rng):
    length = rng.choice((18, 17))
    half = (length + 1) // 2
    while True:
        left = rng.randrange(10 ** (half - 1) + 1, 10**half - 1)
        x = left * 10 ** (length - half) + rng.randrange(10 ** (length - half))
        near = min(abs(mirror(m, length) - x) for m in (left - 1, left, left + 1))
        if near >= GAP:
            return {"n": str(x)}
