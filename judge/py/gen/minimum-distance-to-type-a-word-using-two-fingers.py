"""Minimum Distance to Type a Word Using Two Fingers at the maximum 300 uppercase letters;
trying both fingers for every letter is 2^300."""

from _shapes import random_string

SEEDS = 2


def generate(rng):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return {"word": random_string(rng, letters, 300)}
