"""Number of Orders in the Backlog at 5 * 10^4 orders: buys below and sells above the middle price,
so both backlogs grow to ~2.5 * 10^4 orders, with one order in twenty crossing it; finding the best
order by scanning a backlog costs ~10^9 steps."""

SEEDS = 2
N = 5 * 10**4
MID = 5 * 10**8


def generate(rng):
    orders = []
    for _ in range(N):
        kind = rng.randrange(2)
        if rng.random() < 0.05:
            price = rng.randint(MID // 2, MID + MID // 2)
            amount = rng.randint(1, 10**5)
        else:
            price = rng.randint(1, MID) if kind == 0 else rng.randint(MID + 1, 2 * MID)
            amount = rng.randint(1, 1000)
        orders.append([price, amount, kind])
    if rng.random() < 0.5:
        orders[-1] = [rng.choice((1, 2 * MID)), 10**9, orders[-1][2]]
    return {"orders": orders}
