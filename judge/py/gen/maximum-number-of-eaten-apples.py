"""Maximum Number of Eaten Apples over 10^4 days of large, long-lived harvests, so thousands of
batches are fresh at once and scanning them all each day is quadratic."""

SEEDS = 2
N = 10**4
LIMIT = 2 * 10**4


def generate(rng):
    apples, days = [], []
    for _ in range(N):
        if rng.random() < 0.1:
            apples.append(0)
            days.append(0)
        else:
            apples.append(rng.randint(1, LIMIT))
            days.append(rng.randint(1, LIMIT))
    return {"apples": apples, "days": days}
