"""Count The Repetitions with |s1| = 100 over 2-3 letters, n1 = 10^6 and s2 drawn from the
letters of s1 (often s1 itself), so nearly every character matches and simulating every copy
of s1 costs 10^8 steps with a count of up to 10^6."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
L = 100


def generate(rng):
    s1 = random_string(rng, rng.sample(ascii_lowercase, rng.randint(2, 3)), L)
    s2 = s1 if rng.random() < 0.5 else random_string(rng, sorted(set(s1)), rng.randint(1, L))
    return {"s1": s1, "n1": 10**6, "s2": s2, "n2": rng.randint(1, 100)}
