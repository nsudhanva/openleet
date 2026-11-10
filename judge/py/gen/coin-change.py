"""Coin Change at amount up to 10^4 with 12 coins: small coins (a deep DP), coins where greedy
fails, or only large even coins so an odd amount is unreachable after exploring everything."""

SEEDS = 3


def generate(rng):
    shape = rng.choice(["small", "greedy-trap", "unreachable"])
    if shape == "small":
        coins = rng.sample(range(1, 60), 12)
        amount = 10**4
    elif shape == "greedy-trap":
        coins = [*sorted(rng.sample(range(2, 500), 10)), 997, 1000]
        rng.shuffle(coins)
        amount = rng.randint(9000, 10**4)
    else:
        coins = [2 * c for c in rng.sample(range(1, 50), 11)]
        coins.append(2 * rng.randint(10**8, 10**9))
        amount = rng.randrange(9001, 10**4, 2)
    return {"coins": coins, "amount": amount}
