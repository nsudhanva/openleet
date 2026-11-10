"""Best Time to Buy and Sell Stock III at n = 10^5: random, a zigzag with many candidate
trades, or a long monotone climb where one trade beats two."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.choice(["random", "zigzag", "climb"])
    if shape == "random":
        prices = [rng.randint(0, 10**5) for _ in range(N)]
    elif shape == "zigzag":
        prices = [
            rng.randint(0, 5 * 10**4) if i % 2 else rng.randint(5 * 10**4, 10**5) for i in range(N)
        ]
    else:
        prices = [i * 10**5 // N for i in range(N)]
    return {"prices": prices}
