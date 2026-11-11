"""Maximum XOR With an Element From Array at n = q = 2.5 * 10^4 with most bounds above every
value, so scanning nums for each query costs ~6 * 10^8 steps."""

SEEDS = 2
N = 25000
Q = 25000
LIMIT = 10**9


def generate(rng):
    nums = [rng.randint(0, LIMIT) for _ in range(N)]
    queries = [
        [rng.randint(0, LIMIT), LIMIT if rng.random() < 0.9 else rng.randint(0, LIMIT)]
        for _ in range(Q)
    ]
    return {"nums": nums, "queries": queries}
