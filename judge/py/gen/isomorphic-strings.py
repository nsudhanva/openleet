"""Isomorphic Strings at 5 * 10^4 printable ASCII characters: t a bijective relabelling of s, or
one that maps two letters to the same one far into the string."""

SEEDS = 3
N = 5 * 10**4
ASCII = [chr(c) for c in range(32, 127)]


def generate(rng):
    alpha = rng.sample(ASCII, rng.choice([2, 95]))
    s = [rng.choice(alpha) for _ in range(N)]
    image = ASCII[:]
    rng.shuffle(image)
    mapping = dict(zip(ASCII, image, strict=False))
    t = [mapping[ch] for ch in s]
    shape = rng.randrange(3)
    if shape == 1:
        i = rng.randrange(N - 100, N)
        t[i] = rng.choice([ch for ch in ASCII if ch != t[i]])
    elif shape == 2:
        s[-1] = rng.choice([ch for ch in ASCII if ch not in alpha])
    return {"s": "".join(s), "t": "".join(t)}
