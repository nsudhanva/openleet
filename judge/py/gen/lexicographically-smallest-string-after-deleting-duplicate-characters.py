"""Lexicographically Smallest String After Deleting Duplicate Characters at n = 2 * 10^4: a sorted
first half that is all kept, then random letters with thousands of deletions, so deleting the
first removable descent and rescanning from the front costs ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    letters = "abcdefghijklmnopqrstuvwxyz"
    low = rng.randint(1, 3)
    head = sorted(rng.choice(letters[:low]) for _ in range(N // 2))
    tail = [rng.choice(letters[low - 1 :]) for _ in range(N - N // 2)]
    return {"s": "".join(head + tail)}
