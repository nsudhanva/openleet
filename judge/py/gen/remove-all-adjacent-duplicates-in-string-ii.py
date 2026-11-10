"""Remove Adjacent Duplicates II at length 10^5: nested runs that collapse in a cascade once
the innermost run of k goes, the worst case for repeated rescanning."""

from _shapes import random_string

SEEDS = 2
N = 10**5


def generate(rng):
    k = rng.choice([2, 3, rng.randint(2, 50)])
    if rng.random() < 0.5:
        # Build "a^(k-1) b^(k-1) ... X^k ... b a" style nesting by recursion on a stack.
        s = []
        letters = "abcdefghijklmnopqrstuvwxyz"
        while len(s) < N - 2 * k:
            depth = rng.randint(1, 50)
            chain = [rng.choice(letters)]
            for _ in range(depth - 1):
                chain.append(rng.choice([c for c in letters if c != chain[-1]]))
            if len(s) + 2 * k * depth > N:
                break
            left = [c * rng.randint(1, k - 1) for c in chain[:-1]]
            parts = [*list(left), chain[-1] * k]
            for c, run in zip(reversed(chain[:-1]), reversed(left), strict=False):
                parts.append(c * (k - len(run)))
            s.extend("".join(parts))
        s = "".join(s)
    else:
        s = random_string(rng, "ab", N)
    return {"s": s, "k": k}
