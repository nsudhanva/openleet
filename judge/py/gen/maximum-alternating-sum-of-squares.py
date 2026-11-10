"""Maximum Alternating Sum of Squares at n = 10^5 with values in [-4 * 10^4, 4 * 10^4]
(squares sum past 64-bit-unsafe ranges in other languages)."""

SEEDS = 2
N = 10**5
LIMIT = 4 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    else:
        nums = [rng.choice([-LIMIT, LIMIT, 0, 1]) for _ in range(N)]
    return {"nums": nums}
