"""Number of Unique Flavors After Sharing K Candies at 4 * 10^4 candies with k near half of them, so
counting the flavors left outside every window afresh costs ~4 * 10^8 steps."""

SEEDS = 2
N = 4 * 10**4


def generate(rng):
    flavors = rng.randint(N // 10, N)
    candies = [rng.randint(1, flavors) for _ in range(N)]
    return {"candies": candies, "k": rng.randint(N * 2 // 5, N * 3 // 5)}
