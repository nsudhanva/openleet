"""MagicDictionary with 100 distinct words of up to 100 letters over a tiny alphabet and 100
searches: one-letter edits of dictionary words, exact words, and other lengths."""

SEEDS = 3


def generate(rng):
    alpha = "abcdefghijklmnopqrstuvwxyz"[: rng.choice([2, 3, 26])]
    lengths = [rng.choice([100, rng.randint(1, 100)]) for _ in range(100)]
    words = set()
    for length in lengths:
        for _ in range(50):
            w = "".join(rng.choice(alpha) for _ in range(length))
            if w not in words:
                words.add(w)
                break
    dictionary = sorted(words)
    rng.shuffle(dictionary)
    ops, args = ["MagicDictionary", "buildDict"], [[], [dictionary]]
    for _ in range(100):
        w = list(rng.choice(dictionary))
        kind = rng.randrange(4)
        if kind == 0:
            i = rng.randrange(len(w))
            w[i] = rng.choice("abcdefghijklmnopqrstuvwxyz")
        elif kind == 1 and len(w) > 1:
            i, j = rng.sample(range(len(w)), 2)
            w[i] = rng.choice(alpha)
            w[j] = rng.choice(alpha)
        elif kind == 2:
            w = w[:-1] if len(w) > 1 else [*w, "a"]
        ops.append("search")
        args.append(["".join(w)])
    return {"ops": ops, "args": args}
