"""Count Number of Balanced Permutations at 60 random digits with an even sum, so walking its
distinct permutations is hopeless while the DP over digit counts stays small."""

SEEDS = 2
N = 60


def generate(rng):
    digits = [rng.randrange(10) for _ in range(N)]
    if sum(digits) % 2:
        digits[rng.randrange(N)] ^= 1
    return {"num": "".join(map(str, digits))}
