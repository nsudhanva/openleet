"""Minimum Cost to Separate Sentence Into Rows on twelve sentences of 2500 one-letter words, with
k = 6 to 10 on some (recursing over the row breaks without memoizing is exponential) and k = 1
to 5 on the rest; a DP over all pairs of break points that ignores k is ~3 * 10^6 steps per seed
against ~10^4 for the intended DP, and the seeds add up."""

from _shapes import pick_shape

SEEDS = 12
WORDS = 2500
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    k = rng.randint(6, 10) if pick_shape(rng) == 0 else rng.randint(1, 5)
    return {"sentence": " ".join(rng.choice(LETTERS) for _ in range(WORDS)), "k": k}
