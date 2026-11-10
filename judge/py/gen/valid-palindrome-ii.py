"""Valid Palindrome II at n = 10^5: a palindrome with one extra char inserted where both
skip choices look plausible, so solutions that try only one branch fail."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        # 'a'-heavy palindrome plus one inserted letter: skipping the wrong side looks fine
        # for a long stretch before failing.
        half = ["a" if rng.random() < 0.9 else "b" for _ in range(N // 2 - 1)]
        pal = half + half[::-1]
        i = rng.randrange(len(pal))
        s = [*pal[:i], rng.choice("ab"), *pal[i:]]
    elif shape == 1:
        half = [rng.choice("abc") for _ in range(N // 2)]
        s = half + half[::-1]
        for _ in range(2):  # two mismatches: needs two deletions, answer false
            i = rng.randrange(N // 2)
            s[i] = "d"
    else:
        half = [rng.choice("ab") for _ in range(N // 2)]
        s = [*half, "c", *half[::-1]]
    return {"s": "".join(s)[:N]}
