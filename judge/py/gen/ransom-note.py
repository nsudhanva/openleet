"""Ransom Note with both strings at 10^5 letters: a note that just fits the magazine, or one
short by a single letter."""

from string import ascii_lowercase

SEEDS = 2
N = 10**5


def generate(rng):
    magazine = [rng.choice(ascii_lowercase) for _ in range(N)]
    note = list(magazine)
    rng.shuffle(note)
    if rng.random() < 0.5:
        c = note[0]
        note[0] = next(x for x in ascii_lowercase if x != c and note.count(x) >= magazine.count(x))
    return {"ransomNote": "".join(note), "magazine": "".join(magazine)}
