"""Online Election with 5000 votes and 10^4 queries, close races so the leader changes
often."""

SEEDS = 2
VOTES = 5000
QUERIES = 10**4


def generate(rng):
    candidates = rng.choice([2, 5, VOTES])
    persons = [rng.randrange(candidates) for _ in range(VOTES)]
    times = sorted(rng.sample(range(10**9 // 2), VOTES))
    ops, args = ["TopVotedCandidate"], [[persons, times]]
    for _ in range(QUERIES):
        ops.append("q")
        if rng.random() < 0.3:
            args.append([rng.choice(times)])
        else:
            args.append([rng.randint(times[0], 10**9)])
    return {"ops": ops, "args": args}
