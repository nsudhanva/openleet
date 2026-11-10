"""132 Pattern at n = 2 * 10^5: strictly increasing or decreasing (no pattern, so a quadratic
scan finishes every pair), an increasing run whose only pattern closes at the last element, or
random values."""

SEEDS = 3
N = 2 * 10**5
LIMIT = 10**9


def generate(rng):
    shape = rng.choice(["increasing", "decreasing", "tail", "random"])
    if shape == "increasing":
        start = rng.randint(-LIMIT, LIMIT - 2 * N)
        nums = [start + 2 * i for i in range(N)]
    elif shape == "decreasing":
        start = rng.randint(-LIMIT + 2 * N, LIMIT)
        nums = [start - 2 * i for i in range(N)]
    elif shape == "tail":
        start = rng.randint(-LIMIT, LIMIT - 2 * N)
        nums = [start + 2 * i for i in range(N - 1)]
        nums.append(nums[-2] - 1)
    else:
        nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    return {"nums": nums}
