"""Maximum Number of Events at 10^5 events over 10^5 days: every event spanning the whole
range (a day-by-day scan over all events is quadratic), random intervals, or short events
piled on the same days."""

SEEDS = 3
N = 10**5
DAYS = 10**5


def generate(rng):
    shape = rng.choice(["full", "random", "piled"])
    if shape == "full":
        events = [[rng.randint(1, 10), rng.randint(DAYS - 10, DAYS)] for _ in range(N)]
    elif shape == "piled":
        events = []
        for _ in range(N):
            s = rng.randint(1, 1000)
            events.append([s, min(DAYS, s + rng.randint(0, 5))])
    else:
        events = []
        for _ in range(N):
            s = rng.randint(1, DAYS)
            events.append([s, rng.randint(s, DAYS)])
    return {"events": events}
