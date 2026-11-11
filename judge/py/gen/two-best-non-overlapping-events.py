"""Two Best Non-Overlapping Events at 2 * 10^4 events: random spans over 10^9, so checking every
pair of events is ~2 * 10^8 steps; or events of value 6 * 10^5 and up that all contain one time
plus a few cheap events elsewhere, so scanning pairs from the highest value down still checks
~2 * 10^8 pairs of overlapping events."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4
TOP = 10**9
MIDDLE = TOP // 2
CHEAP = 20


def generate(rng):
    shape = pick_shape(rng)
    events = []
    if shape == 0:
        for _ in range(N):
            start = rng.randint(1, TOP)
            end = min(TOP, start + rng.choice([rng.randint(0, 10**4), rng.randint(0, 10**8)]))
            events.append([start, end, rng.randint(1, 10**6)])
    else:
        for _ in range(N - CHEAP):
            events.append(
                [rng.randint(1, MIDDLE), rng.randint(MIDDLE, TOP), rng.randint(6 * 10**5, 10**6)]
            )
        for _ in range(CHEAP):
            low, high = rng.randint(1, MIDDLE - 10**4), rng.randint(MIDDLE + 10**4, TOP - 10**4)
            start = rng.choice((low, high))
            events.append([start, start + rng.randint(0, 10**4), rng.randint(1, 1000)])
        rng.shuffle(events)
    return {"events": events}
