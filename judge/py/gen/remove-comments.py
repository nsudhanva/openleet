"""Remove Comments with 100 lines of up to 80 characters mixing line comments, multi-line
block comments, "/*/" openers, and comment markers hidden inside other comments; every block
comment is closed."""

from _shapes import random_string

SEEDS = 2
CODE = "abcdefghijklmnopqrstuvwxyz0123456789 ;=+-(){}[],.<>!&|"
INNER = CODE + "/"
LINE_TEXT = CODE + "/*"


def filler(rng, alphabet, n):
    return random_string(rng, alphabet, n)


def generate(rng):
    lines, in_block = [], False
    for _ in range(99):
        line, room = "", rng.randint(0, 80)
        while len(line) < room:
            left = room - len(line)
            if in_block:
                if left >= 2 and rng.random() < 0.3:
                    line += "*/"
                    in_block = False
                else:
                    line += filler(rng, INNER, rng.randint(1, min(12, left)))
                continue
            r = rng.random()
            if r < 0.1 and left >= 2:
                line += "//" + filler(rng, LINE_TEXT, rng.randint(0, left - 2))
                break
            if r < 0.3 and left >= 2:
                line += "/*"
                in_block = True
                if left >= 3 and rng.random() < 0.2:
                    line += "/"
                continue
            line += filler(rng, CODE, rng.randint(1, min(12, left)))
        lines.append(line)
    last = "*/" if in_block else ""
    lines.append(last + filler(rng, CODE, rng.randint(1, 30)))
    return {"source": lines}
