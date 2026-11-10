"""Count Different Palindromic Subsequences at length 1000 over 'abcd': random, or a
repeated palindrome-heavy pattern."""

SEEDS = 2
N = 1000


def generate(rng):
    if rng.random() < 0.5:
        s = "".join(rng.choice("abcd") for _ in range(N))
    else:
        half = "".join(rng.choice("abcd") for _ in range(N // 2))
        s = half + half[::-1]
    return {"s": s}
