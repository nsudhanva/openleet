"""Lexicographically Smallest Valid Sequence with word1 of 3 * 10^5 letters over a tiny alphabet
and word2 a long near-subsequence (one changed letter), or one that cannot be matched."""

SEEDS = 3
N = 3 * 10**5


def generate(rng):
    alpha = "abc"[: rng.choice([2, 3])]
    word1 = [rng.choice(alpha) for _ in range(N)]
    m = rng.choice([N // 3, N - 1, 1000])
    idx = sorted(rng.sample(range(N), m))
    word2 = [word1[i] for i in idx]
    shape = rng.randrange(3)
    if shape == 0:
        j = rng.randrange(m)
        word2[j] = "z"
    elif shape == 1:
        for _ in range(3):
            j = rng.randrange(m)
            word2[j] = "z"
    return {"word1": "".join(word1), "word2": "".join(word2)}
