"""Remove Adjacent Duplicates at length 10^5: a nested palindrome that collapses completely
from the middle out, or random two-letter text with long cascades."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        half = "".join(rng.choice("ab") for _ in range(N // 2))
        s = half + half[::-1]
    else:
        s = "".join(rng.choice("ab") for _ in range(N))
    return {"s": s}
