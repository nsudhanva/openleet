"""Coin Change at amount up to 10^4 with 12 coins, most of them small (below 30), so trying
every count of each coin costs ~10^8 steps: a deep DP, coins where greedy fails, or only even
coins so an odd amount is unreachable after exploring everything."""

SEEDS = 3


def generate(rng):
    shape = rng.choice(["small", "greedy-trap", "unreachable"])
    if shape == "small":
        coins = rng.sample(range(1, 16), 12)
        amount = 10**4
    elif shape == "greedy-trap":
        coins = [*sorted(rng.sample(range(2, 30), 10)), 997, 1000]
        rng.shuffle(coins)
        amount = rng.randint(9000, 10**4)
    else:
        coins = [2 * c for c in rng.sample(range(1, 15), 11)]
        coins.append(2 * rng.randint(10**8, 10**9))
        amount = rng.randrange(9001, 10**4, 2)
    return {"coins": coins, "amount": amount}
