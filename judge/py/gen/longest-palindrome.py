"""Longest Palindrome (letter counts) on 2000 mixed-case letters."""

from _shapes import random_string

SEEDS = 2
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate(rng):
    alphabet = rng.choice([LETTERS, "aA"])
    return {"s": random_string(rng, alphabet, 2000)}
