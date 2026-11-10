"""Longest Absolute File Path on a valid file-system listing close to 10^4 characters with
deep nesting (files are always leaves)."""

from string import ascii_letters, digits

from _shapes import random_string

SEEDS = 2
LIMIT = 9500
CHARS = ascii_letters + digits


def name(rng, low, high):
    return random_string(rng, CHARS, rng.randint(low, high))


def generate(rng):
    lines = []
    total = 0
    depth = 0  # depth the next line may go to (at most one past the last directory)
    deep = rng.random() < 0.5
    while True:
        level = rng.randint(max(0, depth - 3), depth) if deep else rng.randint(0, depth)
        if rng.random() < 0.35:
            entry = name(rng, 1, 12) + "." + name(rng, 1, 4)
            next_depth = level
        else:
            entry = name(rng, 1, 12)
            next_depth = level + 1
        line = "\t" * level + entry
        if total + len(line) + 1 > LIMIT:
            break
        lines.append(line)
        total += len(line) + 1
        depth = next_depth
    return {"input": "\n".join(lines)}
