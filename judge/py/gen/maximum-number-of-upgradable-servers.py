"""Maximum Number of Upgradable Servers with 3000 data centres of 5 * 10^4 to 10^5 servers that
can upgrade about half of them, so counting upgrades one at a time is far too slow."""

SEEDS = 2
N = 3000


def generate(rng):
    count, upgrade, sell, money = [], [], [], []
    for _ in range(N):
        count.append(rng.randint(5 * 10**4, 10**5))
        s = rng.randint(1000, 10**5)
        sell.append(s)
        upgrade.append(max(1, min(10**5, s + rng.randint(-100, 100))))
        money.append(rng.randint(1, 10**5))
    return {"count": count, "upgrade": upgrade, "sell": sell, "money": money}
