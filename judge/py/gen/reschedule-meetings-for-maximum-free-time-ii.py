"""Reschedule Meetings for Maximum Free Time II at n = 10^4 meetings each wider than any gap but
perhaps the last, so searching all gaps for one that fits each meeting costs ~10^8 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    start, end, t = [], [], 0
    for _ in range(N):
        t += rng.randint(0, 1000)
        start.append(t)
        t += rng.randint(1001, 10**4)
        end.append(t)
    last = rng.choice((rng.randint(0, 1000), 10**4))
    return {"eventTime": t + last, "startTime": start, "endTime": end}
