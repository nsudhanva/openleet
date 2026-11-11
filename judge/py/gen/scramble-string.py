"""Scramble String at length 30: one letter repeated around a 4-letter core in the 2413 or 3142
order, which no scramble makes, so every split of the padding passes the letter-count check and
unmemoized recursion runs exponentially long before answering false."""

from string import ascii_lowercase

SEEDS = 3
N = 30


def generate(rng):
    letters = rng.sample(ascii_lowercase, 5)
    pad, core = letters[0], letters[1:]
    order = rng.choice([(1, 3, 0, 2), (2, 0, 3, 1)])
    left = rng.randint(0, N - 4)
    right = N - 4 - left
    s1 = pad * left + "".join(core) + pad * right
    s2 = pad * left + "".join(core[i] for i in order) + pad * right
    return {"s1": s1, "s2": s2}
