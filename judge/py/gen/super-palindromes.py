"""Super Palindromes over ranges spanning up to 10^18 - 1, so only enumerating palindromic
roots (not the range) is fast."""

SEEDS = 3
TOP = 10**18 - 1


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        left, right = 1, TOP
    elif shape == 1:
        left = rng.randint(1, 10**6)
        right = rng.randint(10**17, TOP)
    else:
        a, b = rng.randint(1, TOP), rng.randint(1, TOP)
        left, right = min(a, b), max(a, b)
    return {"left": str(left), "right": str(right)}
