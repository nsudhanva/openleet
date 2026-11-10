"""Maximum Candies for K Children with 10^5 piles up to 10^7 and k up to 10^12, so trying
every pile size linearly is too slow."""

SEEDS = 3
N = 10**5


def generate(rng):
    candies = [rng.randint(1, 10**7) for _ in range(N)]
    total = sum(candies)
    k = rng.choice([10**12, rng.randint(1, total), rng.randint(1, N)])
    return {"candies": candies, "k": k}
