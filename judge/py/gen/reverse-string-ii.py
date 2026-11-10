"""Reverse String II on 10^4 lowercase letters with k small (many chunks), mid, or >= n."""

SEEDS = 3


def generate(rng):
    s = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(10**4))
    k = rng.choice([1, rng.randint(2, 50), rng.randint(51, 9999), 10**4])
    return {"s": s, "k": k}
