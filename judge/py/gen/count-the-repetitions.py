"""Count The Repetitions with |s1| = 100, n1 = 10^6 and a s2 made of the letters of s1: s2 is s1
itself, a run of the commonest letter, or random letters of s1, so nearly every character
matches and simulating every copy of s1 costs 10^8 steps with a count of up to 10^6."""

from string import ascii_lowercase

from _shapes import pick_shape, random_string

SEEDS = 3
L = 100


def generate(rng):
    shape = pick_shape(rng)
    letters = rng.sample(ascii_lowercase, rng.randint(2, 3))
    if shape == 1:
        s1 = "".join(letters[0] if rng.random() < 0.95 else rng.choice(letters) for _ in range(L))
    else:
        s1 = random_string(rng, letters, L)
    if shape == 0:
        s2 = s1
    elif shape == 1:
        s2 = max(set(s1), key=s1.count) * rng.randint(1, 3)
    else:
        s2 = random_string(rng, sorted(set(s1)), rng.randint(1, L))
    return {"s1": s1, "n1": 10**6, "s2": s2, "n2": rng.randint(1, 100)}
