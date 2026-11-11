"""Count Days Without Meetings with 2 * 10^4 meetings over up to 10^9 days: mostly short and
disjoint, a few long, so merging each meeting into a list of disjoint intervals costs ~2 * 10^8
steps and marking days one by one far more."""

SEEDS = 2
N = 2 * 10**4
DAYS = 10**9


def generate(rng):
    days = DAYS if rng.random() < 0.5 else rng.randint(DAYS // 2, DAYS)
    meetings = []
    for _ in range(N):
        length = rng.randint(1, 10**7) if rng.random() < 0.01 else rng.randint(1, 2 * 10**4)
        start = rng.randint(1, days)
        meetings.append([start, min(days, start + length - 1)])
    return {"days": days, "meetings": meetings}
