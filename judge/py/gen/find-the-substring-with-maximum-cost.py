"""s of 5 * 10^4 letters, half of them given costs in [-1000, 1000], so trying every substring
costs ~1.25 * 10^9 steps."""

SEEDS = 2
N = 5 * 10**4
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    chars = "".join(rng.sample(ALPHABET, 13))
    vals = [rng.randint(-1000, 1000) for _ in chars]
    return {
        "s": "".join(rng.choice(ALPHABET) for _ in range(N)),
        "chars": chars,
        "vals": vals,
    }
