"""String Compression at the maximum 2000 chars: long runs (multi-digit counts) or rapid
alternation, so a quadratic in-place shift is punished."""

from _shapes import pick_shape

SEEDS = 3
N = 2000
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"


def generate(rng):
    shape = pick_shape(rng)
    chars = []
    if shape == 0:
        # A few very long runs: counts like 1000 and 999.
        while len(chars) < N:
            c = rng.choice(ALPHABET)
            if chars and chars[-1] == c:
                continue
            chars.extend([c] * min(N - len(chars), rng.randint(1, 1200)))
    elif shape == 1:
        # Runs of length 1-12 mixing single and double digit counts.
        while len(chars) < N:
            c = rng.choice(ALPHABET)
            chars.extend([c] * min(N - len(chars), rng.randint(1, 12)))
    else:
        chars = [rng.choice(ALPHABET) for _ in range(N)]
    return {"chars": chars}
