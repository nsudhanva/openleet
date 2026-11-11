"""Total Appeal of a String at n = 2 * 10^4 over 26 letters, over 4 letters, or over 2 letters
with a third letter only at the very end, so counting the distinct letters of every substring by
extending each start is ~2 * 10^8 steps even when each start stops at the first substring that
holds every letter of s."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 2:
        return {"s": "".join(rng.choice("ab") for _ in range(N - 1)) + "z"}
    alphabet = "abcdefghijklmnopqrstuvwxyz"[: (26, 4)[shape]]
    return {"s": "".join(rng.choice(alphabet) for _ in range(N))}
