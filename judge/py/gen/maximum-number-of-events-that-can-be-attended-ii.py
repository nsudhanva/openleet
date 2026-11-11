"""Maximum Number of Events That Can Be Attended II with 3.5 * 10^4 events on days up to 10^9 that
each span a quarter to three quarters of the timeline and k = 3, so finding each event's next
compatible event by a linear scan is quadratic."""

SEEDS = 2
N = 35 * 10**3
K = 3
SPAN = 10**9


def generate(rng):
    events = []
    for _ in range(N):
        length = rng.randint(SPAN // 4, 3 * SPAN // 4)
        start = rng.randint(1, SPAN - length)
        events.append([start, start + length, rng.randint(1, 10**4)])
    return {"events": events, "k": K}
