"""Minimum Insertion Steps to Make a String Palindrome at length 60 over all 26 letters: ends
rarely match, so recursing on both ways to fix each end without memoization is ~2^60 calls."""

from _shapes import random_string

SEEDS = 2
N = 60


def generate(rng):
    return {"s": random_string(rng, "abcdefghijklmnopqrstuvwxyz", N)}
