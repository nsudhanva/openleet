"""Sell Diminishing-Valued Colored Balls with 2 * 10^4 colors packed just under 10^9 and orders near
10^9, so selling one ball at a time takes ~10^9 steps and every color's level is reached."""

SEEDS = 2
N = 2 * 10**4
TOP = 10**9
SPREAD = 4 * 10**4
MAX_ORDERS = 10**9


def generate(rng):
    if rng.random() < 0.5:
        inventory = [TOP - d for d in rng.sample(range(SPREAD), N)]
    else:
        inventory = [TOP - rng.randrange(SPREAD) for _ in range(N)]
    total = sum(inventory)
    orders = min(total, MAX_ORDERS - rng.randrange(MAX_ORDERS // 10))
    return {"inventory": inventory, "orders": orders}
