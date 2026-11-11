"""Number of Times Binary String Is Prefix-Aligned at the maximum 5 * 10^4 flips, in order apart
from small local shuffles, so checking the whole prefix after every flip costs ~1.25 * 10^9
steps."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    flips = list(range(1, N + 1))
    i = 0
    while i < N:
        width = rng.randint(1, 6)
        block = flips[i : i + width]
        rng.shuffle(block)
        flips[i : i + width] = block
        i += width
    return {"flips": flips}
