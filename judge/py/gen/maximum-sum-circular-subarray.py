"""Maximum Sum Circular Subarray at n = 3 * 10^4: random, all negative, and positive ends
around a negative middle so the best subarray wraps."""

SEEDS = 3
N = 3 * 10**4
LIMIT = 3 * 10**4


def generate(rng):
    kind = rng.choice(("random", "negative", "wrap"))
    if kind == "random":
        nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    elif kind == "negative":
        nums = [rng.randint(-LIMIT, -1) for _ in range(N)]
    else:
        third = N // 3
        nums = (
            [rng.randint(-100, LIMIT) for _ in range(third)]
            + [rng.randint(-LIMIT, 100) for _ in range(N - 2 * third)]
            + [rng.randint(-100, LIMIT) for _ in range(third)]
        )
    return {"nums": nums}
