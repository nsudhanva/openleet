"""Number of Recent Calls with 10^4 pings at tightly packed times, so the 3000 ms window holds
thousands of calls at once."""

SEEDS = 2
CALLS = 10**4


def generate(rng):
    step = rng.choice([1, 3])
    ops, args = ["RecentCounter"], [[]]
    t = rng.randint(1, 1000)
    for _ in range(CALLS):
        ops.append("ping")
        args.append([t])
        t += rng.randint(1, step)
    return {"ops": ops, "args": args}
