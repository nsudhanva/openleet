"""Word Break at |s| = 300 with a dictionary of 1000 words: a run of 'a's ending in 'b'
against every 'a'-word (exponential without memo), or s stitched from dictionary words."""

from _shapes import pick_shape, random_string

SEEDS = 3
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    shape = pick_shape(rng)
    words = {"a" * k for k in range(1, 21)}
    while len(words) < 1000:
        words.add(random_string(rng, "abc", rng.randint(2, 20)))
    words = sorted(words)
    rng.shuffle(words)
    if shape == 0:
        s = "a" * 299 + "b"
    else:
        parts = []
        while sum(map(len, parts)) < 300:
            parts.append(rng.choice(words))
        s = "".join(parts)[:300]
        if shape == 2:
            s = s[:299] + "z"  # no word contains 'z'
    return {"s": s, "wordDict": words}
