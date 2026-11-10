"""Maximum Number of Balloons on 10^4 letters drawn mostly from "balon" with skewed counts."""

SEEDS = 2
N = 10**4


def generate(rng):
    alphabet = "balloon" * 3 + "xyz" if rng.random() < 0.5 else "abcdefghijklmnopqrstuvwxyz"
    return {"text": "".join(rng.choice(alphabet) for _ in range(N))}
