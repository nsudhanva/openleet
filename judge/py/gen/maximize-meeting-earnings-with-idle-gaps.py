"""Maximize Meeting Earnings with Idle Gaps at n = 2 * 10^4: half the meetings short in the first
half of [0, 10^9], half long, starting before the midpoint and ending after it, so the DP over
earlier meetings, or scanning back for the last compatible one, is ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4
SPAN = 10**9


def generate(rng):
    meetings = []
    for _ in range(N):
        start = rng.randrange(SPAN // 2)
        if rng.random() < 0.5:
            end = rng.randint(SPAN // 2 + 1, SPAN)
        else:
            end = start + rng.randint(1, 10**5)
        meetings.append([start, end, rng.randint(1, 10**9)])
    return {"meetings": meetings}
