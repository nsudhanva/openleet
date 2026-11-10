"""Valid Anagram at length 5 * 10^4: a true shuffle, the same with one letter swapped for
another, or strings of different lengths."""

from string import ascii_lowercase

from _shapes import pick_shape

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    s = [rng.choice(ascii_lowercase[: rng.randint(1, 26)]) for _ in range(N)]
    t = s[:]
    rng.shuffle(t)
    if shape == 1:
        i = rng.randrange(N)
        t[i] = ascii_lowercase[(ascii_lowercase.index(t[i]) + 1) % 26]
    elif shape == 2:
        t.pop()
    return {"s": "".join(s), "t": "".join(t)}
