"""Best Time to Buy and Sell Stock with Transaction Fee at n = 5 * 10^4: random prices with a
fee from 0 to near the cap, so some trades are worth it and some are not."""

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        prices = [rng.randint(1, 5 * 10**4 - 1) for _ in range(N)]
    else:
        prices = [
            rng.randint(1, 100) if i % 2 == 0 else rng.randint(1, 5 * 10**4 - 1) for i in range(N)
        ]
    fee = rng.choice([0, rng.randint(0, 100), rng.randint(0, 5 * 10**4 - 1)])
    return {"prices": prices, "fee": fee}
