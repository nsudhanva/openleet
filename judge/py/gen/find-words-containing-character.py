"""Find Words Containing Character at the maximum 50 words of 50 letters."""

SEEDS = 2


def generate(rng):
    alpha = "abcdefghijklmnopqrstuvwxyz"[: rng.choice([3, 26])]
    words = ["".join(rng.choice(alpha) for _ in range(rng.randint(1, 50))) for _ in range(50)]
    return {"words": words, "x": rng.choice(alpha)}
