"""Maximum Running Time of N Computers with 2000 batteries of up to 10^9 minutes, so the answer is
in the hundreds of millions and trying each running time in turn cannot finish."""

SEEDS = 2
M = 2000
LIMIT = 10**9


def generate(rng):
    batteries = [rng.randint(1, LIMIT) for _ in range(M)]
    return {"n": rng.randint(max(1, M // 10), M // 2), "batteries": batteries}
