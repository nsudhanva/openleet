"""Longest Palindrome by Concatenating Two Letter Words at the maximum n = 10^5, half of the words
without their reverse anywhere, so searching the list for each word's partner costs ~10^10
comparisons."""

SEEDS = 2
N = 10**5


def generate(rng):
    # Words over 'a'-'m' then 'n'-'z' never meet their reverse; mixed and doubled words pair up.
    lo, hi = "abcdefghijklm", "nopqrstuvwxyz"
    words = [rng.choice(lo) + rng.choice(hi) for _ in range(N // 2)]
    while len(words) < N:
        a = rng.choice(lo + hi)
        b = a if rng.random() < 0.3 else rng.choice(lo + hi)
        if a < b and b in hi and a in lo:
            b, a = a, b
        words.append(a + b)
    rng.shuffle(words)
    return {"words": words}
