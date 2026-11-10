"""Word Pattern near the limits (300 pattern letters, 3000-char sentence): a true bijection,
two letters mapped to the same word, or a word-count mismatch."""

from string import ascii_lowercase

from _shapes import pick_shape, random_string

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    pattern = [rng.choice(ascii_lowercase) for _ in range(300)]
    used = sorted(set(pattern))
    names = set()
    while len(names) < len(used):
        names.add(random_string(rng, "xyz", rng.randint(1, 8)))
    mapping = dict(zip(used, sorted(names), strict=True))
    if shape == 1 and len(used) > 1:
        mapping[used[1]] = mapping[used[0]]  # not a bijection
    words = [mapping[c] for c in pattern]
    if shape == 2:
        words.pop()
    s = " ".join(words)
    while len(s) > 3000:
        words = [w[:1] for w in words]
        s = " ".join(words)
    return {"pattern": "".join(pattern), "s": s}
