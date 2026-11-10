"""Valid Palindrome at 2 * 10^5 printable ASCII chars: an alphanumeric palindrome buried in
punctuation and mixed case, sometimes with one mismatch in the middle."""

from string import ascii_lowercase, digits

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**5
ALNUM = ascii_lowercase + digits
JUNK = " ,.:;!?'\"-_()[]{}@#$%^&*/\\|`~<>+="


def generate(rng):
    shape = pick_shape(rng)
    if shape == 2:
        return {"s": "".join(chr(rng.randint(32, 126)) for _ in range(N))}
    half = [rng.choice(ALNUM) for _ in range(N // 4)]
    core = half + half[::-1]
    if shape == 1:
        mid = len(half)
        core[mid] = "x" if core[mid] != "x" else "y"
    out = []
    for ch in core:
        while rng.random() < 0.5 and len(out) < N - len(core):
            out.append(rng.choice(JUNK))
        out.append(ch.upper() if rng.random() < 0.5 else ch)
    return {"s": "".join(out)[:N]}
