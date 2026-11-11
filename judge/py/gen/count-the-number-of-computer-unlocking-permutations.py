"""Count the Number of Computer Unlocking Permutations at n = 10^5 with computer 0 the unique
easiest, so the answer is (n - 1)! mod 10^9 + 7 and multiplying it out without the modulus
handles numbers of ~450,000 digits."""

SEEDS = 2
N = 10**5
LIMIT = 10**6


def generate(rng):
    first = rng.randint(1, 1000)
    rest = [rng.randint(first + 1, LIMIT) for _ in range(N - 1)]
    return {"complexity": [first, *rest]}
