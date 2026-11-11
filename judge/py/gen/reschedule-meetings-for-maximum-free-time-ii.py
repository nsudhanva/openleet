"""Reschedule Meetings for Maximum Free Time II at n = 3 * 10^4 meetings each wider than any gap,
and a last gap that is also too small on two shapes out of three (on the third it fits every
meeting), so searching all gaps for one that fits each meeting costs ~4.5 * 10^8 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 3 * 10**4


def generate(rng):
    start, end, t = [], [], 0
    for _ in range(N):
        t += rng.randint(0, 1000)
        start.append(t)
        t += rng.randint(1001, 5000)
        end.append(t)
    last = 5000 if pick_shape(rng) == 2 else rng.randint(0, 1000)
    return {"eventTime": t + last, "startTime": start, "endTime": end}
