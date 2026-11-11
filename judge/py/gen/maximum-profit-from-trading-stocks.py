"""Maximum Profit From Trading Stocks with 200 cheap stocks and budget 1000, so almost every
subset is affordable and enumerating them cannot finish."""

SEEDS = 2
N = 200
BUDGET = 1000


def generate(rng):
    present = [rng.randint(0, 40) for _ in range(N)]
    future = [rng.randint(0, 100) for _ in range(N)]
    return {"present": present, "future": future, "budget": BUDGET}
