"""Longest Palindrome (letter counts) on 2000 mixed-case letters."""

from string import ascii_letters

from _shapes import random_string

SEEDS = 2


def generate(rng):
    alphabet = rng.choice([ascii_letters, "aA"])
    return {"s": random_string(rng, alphabet, 2000)}
