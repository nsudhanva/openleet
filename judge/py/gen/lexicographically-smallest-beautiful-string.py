"""Lexicographically Smallest Beautiful String at the maximum length 10^5 built from the top three
of the k letters so that no position but the first one or two can grow, so rebuilding and
rechecking the whole string at each position costs ~10^10 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    k = rng.randint(4, 26)
    t1, t2, t3 = (chr(ord("a") + k - 3 + i) for i in range(3))
    # t2 t3 t1 repeated: every letter above s[i] is one of the two letters before it.
    pattern = (t2, t3, t1)
    shift = rng.randrange(3)
    return {"s": "".join(pattern[(i + shift) % 3] for i in range(N)), "k": k}
