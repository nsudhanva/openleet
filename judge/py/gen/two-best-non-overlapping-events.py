"""Two Best Non-Overlapping Events at 2 * 10^4 events of random spans over 10^9, so checking
every pair of events is ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
TOP = 10**9


def generate(rng):
    events = []
    for _ in range(N):
        start = rng.randint(1, TOP)
        end = min(TOP, start + rng.choice([rng.randint(0, 10**4), rng.randint(0, 10**8)]))
        events.append([start, end, rng.randint(1, 10**6)])
    return {"events": events}
