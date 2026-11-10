"""Most Common Word on a paragraph of up to 1000 characters with mixed case and punctuation,
a banned word that is the most frequent overall, and one unique most frequent unbanned word."""

from _shapes import random_string

SEEDS = 3
MARKS = "!?',;."


def generate(rng):
    vocab = {random_string(rng, "abcdefgh", rng.randint(1, 6)) for _ in range(60)}
    vocab = sorted(vocab)
    rng.shuffle(vocab)
    banned_word, winner = vocab[0], vocab[1]
    others = vocab[2:]
    words = [banned_word] * 40 + [winner] * 30
    counts = {}
    for _ in range(400):
        w = rng.choice(others)
        if counts.get(w, 0) < 25:
            counts[w] = counts.get(w, 0) + 1
            words.append(w)
    rng.shuffle(words)
    tokens = []
    for w in words:
        token = "".join(ch.upper() if rng.random() < 0.3 else ch for ch in w)
        tokens.append(
            (w in (banned_word, winner), token + (rng.choice(MARKS) if rng.random() < 0.2 else ""))
        )
    room = 1000 - sum(len(t) + 1 for keep, t in tokens if keep)
    parts = []
    for keep, token in tokens:
        if not keep:
            if len(token) + 1 > room:
                continue
            room -= len(token) + 1
        parts.append(token)
    banned = {banned_word, *rng.sample(others, rng.randint(0, 20))}
    return {"paragraph": " ".join(parts), "banned": sorted(banned)}
