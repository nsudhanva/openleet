"""Longest Ideal Subsequence at n = 2 * 10^4: one letter only at index 0 and the rest drawn from
the letters within k of it, so a DP that scans earlier indices backwards until it has seen every
nearby letter still reaches index 0, ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    k = rng.randint(1, 6)
    letters = "abcdefghijklmnopqrstuvwxyz"
    rare = rng.randrange(k, 26 - k)
    pool = [letters[i] for i in range(rare - k, rare + k + 1) if i != rare]
    return {"s": letters[rare] + "".join(rng.choice(pool) for _ in range(N - 1)), "k": k}
