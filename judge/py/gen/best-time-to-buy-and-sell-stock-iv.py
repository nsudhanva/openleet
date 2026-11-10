"""Best Time to Buy and Sell Stock IV at n = 1000 and k up to 100: a zigzag with ~500 profitable
trades (more than k, so the DP must choose), or random prices."""

SEEDS = 3
N = 1000


def generate(rng):
    if rng.random() < 0.5:
        prices = [rng.randint(0, 400) if i % 2 == 0 else rng.randint(600, 1000) for i in range(N)]
    else:
        prices = [rng.randint(0, 1000) for _ in range(N)]
    return {"k": rng.choice([100, rng.randint(1, 100)]), "prices": prices}
