"""Check If Digits Are Equal in String After Operations II at n = 2 * 10^4 random digits, the
last one sometimes set so the final two digits match, so simulating the n - 2 rounds is
quadratic."""

from math import comb

SEEDS = 2
N = 2 * 10**4


def binom_mod5(n, k):
    """C(n, k) mod 5 by Lucas's theorem."""
    out = 1
    while n or k:
        out = out * comb(n % 5, k % 5) % 5
        n, k = n // 5, k // 5
    return out


def generate(rng):
    digits = [rng.randrange(10) for _ in range(N)]
    if rng.random() < 0.5:
        # The final digits are sum C(N-2, i) * d[i] and sum C(N-2, i) * d[i+1] mod 10, and
        # the last digit enters only the second, with coefficient 1.
        n = N - 2
        coef = [(5 * ((k & (n - k)) == 0) + 6 * binom_mod5(n, k)) % 10 for k in range(n + 1)]
        first = sum(c * d for c, d in zip(coef, digits, strict=False)) % 10
        rest = sum(c * d for c, d in zip(coef, digits[1:-1], strict=False)) % 10
        digits[-1] = (first - rest) % 10
    return {"s": "".join(map(str, digits))}
