"""Count Substrings Divisible By Last Digit at length 4 * 10^4, about a third of the digits 7 (the
one last digit with no digit-rule shortcut), so testing every substring costs 8 * 10^8 steps."""

SEEDS = 2
N = 4 * 10**4


def generate(rng):
    digits = "0123456789777"
    return {"s": "".join(rng.choice(digits) for _ in range(N))}
