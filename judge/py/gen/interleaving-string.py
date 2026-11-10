"""Interleaving String at the maximum lengths (100 + 100 = 200) over one or two letters, so many
split choices look valid; s3 is a true interleaving or one with a letter changed."""

from _shapes import random_string

SEEDS = 3


def generate(rng):
    alpha = rng.choice(["a", "ab"])
    s1 = random_string(rng, alpha, 100)
    s2 = random_string(rng, alpha, 100)
    picks = [0] * 100 + [1] * 100
    rng.shuffle(picks)
    out, i, j = [], 0, 0
    for p in picks:
        if p == 0:
            out.append(s1[i])
            i += 1
        else:
            out.append(s2[j])
            j += 1
    if rng.random() < 0.5:
        k = rng.randrange(200)
        out[k] = "b" if out[k] != "b" else "c"
    return {"s1": s1, "s2": s2, "s3": "".join(out)}
