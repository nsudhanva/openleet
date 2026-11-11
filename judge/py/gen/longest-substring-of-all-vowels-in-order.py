"""Longest Substring Of All Vowels in Order at 3 * 10^4 letters: one beautiful run of ~80% of the
word (the answer) amid random vowels, so extending from every start is ~10^8 steps."""

SEEDS = 2
N = 3 * 10**4
VOWELS = "aeiou"


def _noise(rng, length):
    return "".join(rng.choice(VOWELS) for _ in range(length))


def generate(rng):
    block = N * 4 // 5
    cuts = sorted(rng.sample(range(1, block), 4))
    runs = [b - a for a, b in zip([0, *cuts], [*cuts, block], strict=True)]
    big = "".join(v * r for v, r in zip(VOWELS, runs, strict=True))
    before = rng.randrange(N - block + 1)
    # Noise ends in 'u' before the run and starts with 'e' after it, so it cannot extend it.
    head = _noise(rng, before - 1) + "u" if before else ""
    tail_len = N - block - before
    tail = "e" + _noise(rng, tail_len - 1) if tail_len else ""
    return {"word": head + big + tail}
