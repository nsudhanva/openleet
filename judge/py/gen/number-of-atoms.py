"""Number of Atoms on valid formulas of close to 1000 characters with nested, multiplied
groups; the generator tracks every count so the totals stay within 32 bits."""

from string import ascii_lowercase, ascii_uppercase

from _shapes import random_string

SEEDS = 3
MAX_LEN = 1000
CAP = 2**31 - 1


def generate(rng):
    names = sorted(
        {
            rng.choice(ascii_uppercase) + random_string(rng, ascii_lowercase, rng.randint(0, 2))
            for _ in range(40)
        }
    )
    big = rng.random() < 0.5

    def count(depth):
        if rng.random() < 0.4:
            return 1
        return rng.randint(2, 10**4 if big and depth == 0 else 9)

    def group(depth, budget):
        """(text, {atom: count}) of a non-empty formula at most `budget` characters long."""
        text, atoms = "", {}
        while len(text) < budget:
            room = budget - len(text)
            if depth < 6 and room >= 10 and rng.random() < 0.25:
                inner, inner_atoms = group(depth + 1, rng.randint(1, min(room - 7, 200)))
                k = count(depth)
                piece = "(" + inner + ")" + (str(k) if k > 1 else "")
                add = {a: c * k for a, c in inner_atoms.items()}
            else:
                name = rng.choice(names)
                k = count(depth)
                piece = name + (str(k) if k > 1 else "")
                add = {name: k}
            if len(piece) > room:
                break
            text += piece
            for a, c in add.items():
                atoms[a] = atoms.get(a, 0) + c
            if depth and rng.random() < 0.1:
                break
        if not text:
            name = rng.choice([n for n in names if len(n) == 1] or ["H"])
            text, atoms = name, {name: 1}
        return text, atoms

    while True:
        text, atoms = group(0, MAX_LEN)
        if max(atoms.values()) <= CAP and len(text) <= MAX_LEN:
            return {"formula": text}
