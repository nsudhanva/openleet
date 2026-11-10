"""Count Palindromic Subsequences (length 5) on a 10^4-digit string: all ten digits at random,
or only two digits so counts are enormous before the modulo."""

SEEDS = 2
N = 10**4


def generate(rng):
    alphabet = "0123456789" if rng.random() < 0.5 else "".join(rng.sample("0123456789", 2))
    return {"s": "".join(rng.choice(alphabet) for _ in range(N))}
