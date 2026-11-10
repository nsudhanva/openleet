"""Remove Duplicate Letters at length 10^4 over all 26 letters, with letters' last occurrences
spread to the end so the monotonic stack keeps popping."""

from string import ascii_lowercase

SEEDS = 2


def generate(rng):
    if rng.random() < 0.5:
        s = [rng.choice(ascii_lowercase) for _ in range(10**4 - 26)]
        tail = list(ascii_lowercase)
        rng.shuffle(tail)
        s += tail
    else:
        s = list(ascii_lowercase[::-1] * (10**4 // 26))
        s += [rng.choice(ascii_lowercase) for _ in range(10**4 - len(s))]
    return {"s": "".join(s)}
