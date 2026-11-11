"""Last Substring in Lexicographical Order at the maximum length 4 * 10^5, the block c c d
repeated and ending in c c e with d < e < c, so every block start is a candidate sharing a long
prefix with the others and comparing candidates costs ~10^10 character steps."""

SEEDS = 2
N = 4 * 10**5


def generate(rng):
    # Every run of the largest letter has the same length, and the answer is the last block.
    letters = "abcdefghijklmnopqrstuvwxyz"
    d, e, c = sorted(rng.sample(letters, 3))
    return {"s": (c + c + d) * (N // 3 - 1) + c + c + e}
