"""Divide Chocolate at n = 10^4 with k between 1 and 50, so the answer is at least 10^7 and
trying every candidate sweetness in turn costs answer * n."""

SEEDS = 2
N = 10**4


def generate(rng):
    sweetness = [rng.randint(1, 10**5) for _ in range(N)]
    return {"sweetness": sweetness, "k": rng.randint(1, min(50, N - 1))}
