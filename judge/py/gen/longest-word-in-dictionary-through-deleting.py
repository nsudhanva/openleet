"""Longest Word Through Deleting with s of length 1000 and 1000 dictionary words, many of them
long subsequences of s (checking each costs up to 1000 steps)."""

SEEDS = 2
N = 1000


def generate(rng):
    alphabet = rng.choice(["ab", "abcde"])
    s = "".join(rng.choice(alphabet) for _ in range(N))
    dictionary = []
    total = 0
    for _ in range(N):
        if rng.random() < 0.5:
            keep = rng.randint(1, min(N, 2000))
            idx = sorted(rng.sample(range(N), min(keep, N)))
            word = "".join(s[i] for i in idx[: rng.randint(1, len(idx))])
        else:
            word = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, N)))
        if total + len(word) > 6 * 10**5:
            word = word[:20]
        total += len(word)
        dictionary.append(word)
    return {"s": s, "dictionary": dictionary}
