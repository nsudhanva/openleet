"""Verifying an Alien Dictionary at the maximum 100 words of up to 20 letters: sorted under a
random order with long shared prefixes, sometimes with a prefix placed after its extension."""

from _shapes import pick_shape, random_string

SEEDS = 3
N = 100
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    shape = pick_shape(rng)
    order = list(LETTERS)
    rng.shuffle(order)
    rank = {c: i for i, c in enumerate(order)}
    prefix = random_string(rng, LETTERS, rng.randint(0, 15))
    words = [(prefix + random_string(rng, LETTERS[:5], rng.randint(1, 5)))[:20] for _ in range(N)]
    words.sort(key=lambda w: [rank[c] for c in w])
    if shape == 1:
        i = rng.randrange(N - 1)
        words[i], words[i + 1] = words[i + 1], words[i]
    elif shape == 2:
        w = words[N // 2]
        words[N // 2] = w + rng.choice(LETTERS) if len(w) < 20 else w
        words[N // 2 + 1] = w  # the shorter prefix now comes after its extension
    return {"words": words, "order": "".join(order)}
