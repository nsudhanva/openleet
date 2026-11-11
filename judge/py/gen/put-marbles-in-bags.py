"""Put Marbles in Bags at the maximum 10^5 weights with k = 5 * 10^4 bags, so picking the k - 1
largest and smallest adjacent sums one at a time does ~10^10 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    return {
        "weights": [rng.randint(1, 10**9) for _ in range(N)],
        "k": N // 2 + rng.randrange(N // 10),
    }
