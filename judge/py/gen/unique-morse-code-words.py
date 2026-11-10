"""Unique Morse Code Words at 100 words of up to 12 letters, including different words with
the same Morse transformation."""

SEEDS = 2
N = 100


def generate(rng):
    # 'n' (-.) + 'e' (.) equals 'd' (-..); mix such collisions with random words.
    pieces = ["d", "ne", "te", "a", "et", "ee", "i", "m", "tt"]
    words = []
    for _ in range(N):
        if rng.random() < 0.5:
            w = ""
            while len(w) < 10:
                w += rng.choice(pieces)
            words.append(w[:12])
        else:
            words.append(
                "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rng.randint(1, 12)))
            )
    return {"words": words}
