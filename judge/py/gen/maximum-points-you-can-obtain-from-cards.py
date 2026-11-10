"""Maximum Points You Can Obtain from Cards at n = 10^5 with k near n / 2 or n - 1, so
trying every split by re-summing is quadratic."""

SEEDS = 3
N = 10**5


def generate(rng):
    cards = [rng.randint(1, 10**4) for _ in range(N)]
    k = rng.choice([N // 2, N - 1, rng.randint(1, N)])
    return {"cardPoints": cards, "k": k}
