"""Total Appeal of a String at n = 2 * 10^4, so counting the distinct letters of every substring
by extending each start is ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    alphabet = "abcdefghijklmnopqrstuvwxyz"[: rng.choice((26, 4))]
    return {"s": "".join(rng.choice(alphabet) for _ in range(N))}
