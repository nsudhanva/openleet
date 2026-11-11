"""Palindrome Permutation II at the maximum 16 letters, eight distinct pairs (or seven, one of
them doubled), so permuting the whole string tries up to 16! orders for at most 8! = 40,320
palindromes."""

SEEDS = 2


def generate(rng):
    letters = rng.sample("abcdefghijklmnopqrstuvwxyz", 8)
    if rng.random() < 0.5:
        letters[-1] = letters[0]
    s = list("".join(c * 2 for c in letters))
    rng.shuffle(s)
    return {"s": "".join(s)}
