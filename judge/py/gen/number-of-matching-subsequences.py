"""Number of Matching Subsequences with |s| = 5 * 10^4 and 5000 words of up to 50 letters,
most of them real subsequences ending near the end of s, so scanning s once per word is
2.5 * 10^8 steps."""

SEEDS = 3
N = 5 * 10**4
WORDS = 5000


def generate(rng):
    alphabet = rng.choice(("ab", "abcde", "abcdefghijklmnopqrstuvwxyz"))
    s = "".join(rng.choice(alphabet) for _ in range(N))
    words = []
    for _ in range(WORDS):
        length = rng.randint(1, 50)
        if rng.random() < 0.7:
            picks = sorted(rng.sample(range(N), length))
            picks[-1] = max(picks[-1], N - 1 - rng.randint(0, 10))
            picks = sorted(set(picks))
            words.append("".join(s[i] for i in picks))
        else:
            words.append("".join(rng.choice(alphabet) for _ in range(length)))
    return {"s": s, "words": words}
