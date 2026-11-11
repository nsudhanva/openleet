"""Check If a String Contains All Binary Codes of Size K at k = 17: a randomly rotated and
complemented de Bruijn sequence (every code exactly once) padded with random bits, so searching
the string for each of the 2^17 codes is quadratic."""

SEEDS = 2
K = 17
MAX_LEN = 5 * 10**5


def de_bruijn(k):
    """The binary de Bruijn sequence of order k: Lyndon words of length dividing k, in order."""
    seq, word = [], [-1]
    while word:
        word[-1] += 1
        size = len(word)
        if k % size == 0:
            seq += word
        while len(word) < k:
            word.append(word[len(word) - size])
        while word and word[-1] == 1:
            word.pop()
    return seq


def generate(rng):
    seq = de_bruijn(K)
    cut = rng.randrange(len(seq))
    seq = seq[cut:] + seq[:cut]
    flip = rng.randrange(2)
    s = "".join("01"[b ^ flip] for b in seq + seq[: K - 1])
    pad = rng.randint(0, min(len(s), MAX_LEN - len(s)))
    if rng.random() < 0.5:
        s += "".join(rng.choice("01") for _ in range(pad))
    else:
        s = "".join(rng.choice("01") for _ in range(pad)) + s
    return {"s": s, "k": K}
