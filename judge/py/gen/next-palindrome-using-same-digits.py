"""Next Palindrome Using Same Digits at 10^5 digits: the first half is a smaller digit then the
rest in non-increasing order, so the next permutation pivots at the very front and a search
that tries each position against its whole suffix is ~1.25 * 10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    n = N - rng.randrange(2)
    half = sorted((rng.choice("23456789") for _ in range(n // 2 - 1)), reverse=True)
    half = [rng.choice("12"), *half]
    mid = [rng.choice("0123456789")] if n % 2 else []
    return {"num": "".join(half + mid + half[::-1])}
