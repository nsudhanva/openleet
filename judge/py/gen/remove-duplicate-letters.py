"""Remove Duplicate Letters at length 10^4 over all 26 letters, with letters' last occurrences
spread to the end so the monotonic stack keeps popping."""

SEEDS = 2
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    if rng.random() < 0.5:
        s = [rng.choice(LETTERS) for _ in range(10**4 - 26)]
        tail = list(LETTERS)
        rng.shuffle(tail)
        s += tail
    else:
        s = list(LETTERS[::-1] * (10**4 // 26))
        s += [rng.choice(LETTERS) for _ in range(10**4 - len(s))]
    return {"s": "".join(s)}
