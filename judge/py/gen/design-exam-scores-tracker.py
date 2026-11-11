"""Exam Scores Tracker with 4 * 10^4 calls: 1.6 * 10^4 records, then mostly totalScore over either
a wide range or a narrow one mid-way, so summing the range per query or walking in from both ends
to find its edges costs ~2 * 10^8 steps."""

SEEDS = 2
CALLS = 4 * 10**4
FILL = 16000
STEP = 5  # the most one record's time moves past the last; small steps keep the JSON short
SCORE = 1000


def generate(rng):
    ops, args = ["ExamTracker"], [[]]
    times = []
    t = 0
    for _ in range(FILL):
        t += rng.randint(1, STEP)
        times.append(t)
        ops.append("record")
        args.append([t, rng.randint(1, SCORE)])
    for _ in range(CALLS - FILL):
        if rng.random() < 0.9:
            n = len(times)
            if rng.random() < 0.3:  # wide: from the first tenth to the last tenth
                lo = rng.randint(1, times[n // 10])
                hi = rng.randint(times[-(n // 10)], t)
            else:  # narrow, around the middle
                lo = rng.randint(times[n * 9 // 20], times[n // 2])
                hi = rng.randint(lo, times[n * 11 // 20])
            ops.append("totalScore")
            args.append([lo, hi])
        else:
            t += rng.randint(1, STEP)
            times.append(t)
            ops.append("record")
            args.append([t, rng.randint(1, SCORE)])
    return {"ops": ops, "args": args}
