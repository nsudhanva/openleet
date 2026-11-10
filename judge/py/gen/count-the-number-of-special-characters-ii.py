"""Count the Number of Special Characters II at length 2 * 10^5: random mixed case, or all
lowercase first then all uppercase (every letter special)."""

SEEDS = 2
N = 2 * 10**5
LOWER = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    if rng.random() < 0.5:
        word = "".join(rng.choice(LOWER + LOWER.upper()) for _ in range(N))
    else:
        half = N // 2
        word = "".join(rng.choice(LOWER) for _ in range(half))
        word += "".join(rng.choice(LOWER.upper()) for _ in range(N - half))
    return {"word": word}
