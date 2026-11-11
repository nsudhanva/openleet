"""Reschedule Meetings for Maximum Free Time I at n = 3 * 10^4 meetings with k = n / 2 or n / 3,
so summing every window of k + 1 gaps afresh costs ~2 * 10^8 additions."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    k = N // rng.choice((2, 3))
    start, end, t = [], [], 0
    for _ in range(N):
        t += rng.randint(0, 10**4)
        start.append(t)
        t += rng.randint(1, 10**4)
        end.append(t)
    return {"eventTime": t + rng.randint(0, 10**4), "k": k, "startTime": start, "endTime": end}
