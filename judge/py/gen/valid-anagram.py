"""Valid Anagram at length 5 * 10^4: a true shuffle, the same with one letter swapped for
another, or strings of different lengths."""

SEEDS = 3
N = 5 * 10**4
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    s = [rng.choice(LETTERS[: rng.randint(1, 26)]) for _ in range(N)]
    t = s[:]
    rng.shuffle(t)
    if shape == 1:
        i = rng.randrange(N)
        t[i] = LETTERS[(LETTERS.index(t[i]) + 1) % 26]
    elif shape == 2:
        t.pop()
    return {"s": "".join(s), "t": "".join(t)}
