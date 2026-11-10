"""Minimum Distance to Type a Word Using Two Fingers at the maximum 300 uppercase letters;
trying both fingers for every letter is 2^300."""

SEEDS = 2


def generate(rng):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return {"word": "".join(rng.choice(letters) for _ in range(300))}
