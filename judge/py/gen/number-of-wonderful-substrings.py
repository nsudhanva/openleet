"""Number of Wonderful Substrings at 2 * 10^4 letters from 'a' to 'j', so extending a parity mask
from every start costs 2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    alphabet = "abcdefghij"[: rng.randint(2, 10)]
    return {"word": "".join(rng.choice(alphabet) for _ in range(N))}
