"""Word Subsets at 10^4 words on each side, where checking every pair is 10^8 comparisons;
words2 demands that only some of words1 meet."""

SEEDS = 2
N = 10**4
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    narrow = rng.random() < 0.5
    alpha1 = "abcdef" if narrow else LETTERS
    words1 = set()
    while len(words1) < N:
        words1.add("".join(rng.choice(alpha1) for _ in range(rng.randint(1, 10))))
    words1 = sorted(words1)
    rng.shuffle(words1)
    words2 = ["".join(rng.choice("abc") for _ in range(rng.randint(1, 2))) for _ in range(N)]
    return {"words1": words1, "words2": words2}
