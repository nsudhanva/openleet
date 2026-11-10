"""Substring with Concatenation at |s| = 10^4: one letter repeated with 5000 one-letter words
(every window is a match), or s stitched from a small vocabulary with many words, punishing
per-index rescans."""

SEEDS = 3
N = 10**4


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        return {"s": "a" * N, "words": ["a"] * rng.randint(2000, 5000)}
    width = rng.randint(1, 3) if shape == 1 else rng.randint(5, 30)
    letters = "ab" if shape == 1 else "abc"
    vocab = sorted({"".join(rng.choice(letters) for _ in range(width)) for _ in range(6)})
    count = rng.randint(N // width // 4, N // width // 2)
    count = max(1, min(count, 5000))
    words = [rng.choice(vocab) for _ in range(count)]
    pieces = []
    while len(pieces) * width < N // width * width:
        if rng.random() < 0.3:
            block = words[:]
            rng.shuffle(block)
            pieces.extend(block)
        else:
            pieces.append(rng.choice(vocab))
    s = "".join(pieces)[:N]
    s = s[rng.randrange(width) :] if width > 1 else s
    return {"s": s, "words": words}
