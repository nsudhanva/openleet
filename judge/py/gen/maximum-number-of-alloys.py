"""Maximum Number of Alloys with 20 machines and metals, cheap compositions and a budget of 10^8,
so every machine can make about 10^6 alloys and counting them one at a time cannot finish."""

SEEDS = 2
N = K = 20
BUDGET = 10**8


def generate(rng):
    composition = [[rng.randint(1, 3) for _ in range(N)] for _ in range(K)]
    stock = [rng.randint(0, 1000) for _ in range(N)]
    cost = [rng.randint(1, 3) for _ in range(N)]
    budget = rng.randint(BUDGET * 9 // 10, BUDGET)
    return {
        "n": N,
        "k": K,
        "budget": budget,
        "composition": composition,
        "stock": stock,
        "cost": cost,
    }
