"""Resulting String After Adjacent Removals at n = 2 * 10^4: a half with no removable pair, then
its mirror image that cancels it pair by pair from the middle, so rescanning for the leftmost
pair after each removal costs ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4
ABC = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    left = [rng.randrange(26)]
    while len(left) < N // 2:
        c = rng.randrange(26)
        if (c - left[-1]) % 26 not in (1, 25):
            left.append(c)
    right = [(c + rng.choice((1, 25))) % 26 for c in reversed(left)]
    cut = rng.randrange(N // 10)
    # Dropping the last `cut` letters of the mirror leaves the first `cut` letters standing.
    return {"s": "".join(ABC[c] for c in left + right[: len(right) - cut])}
