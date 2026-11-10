"""Longest Arithmetic Subsequence of Given Difference at n = 10^5, values in [-10^4, 10^4]:
random values, or a long progression interleaved with noise (quadratic DP times out)."""

SEEDS = 3
N = 10**5
LIMIT = 10**4


def generate(rng):
    difference = rng.choice([0, 1, -1, rng.randint(-LIMIT, LIMIT)])
    if rng.random() < 0.4:
        arr = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    else:
        arr = []
        cur = rng.randint(-LIMIT, LIMIT)
        for _ in range(N):
            if rng.random() < 0.5:
                arr.append(cur)
                if -LIMIT <= cur + difference <= LIMIT:
                    cur += difference
            else:
                arr.append(rng.randint(-LIMIT, LIMIT))
    return {"arr": arr, "difference": difference}
