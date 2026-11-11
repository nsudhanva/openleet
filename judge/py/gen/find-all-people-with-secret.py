"""Find All People With Secret with n = 4 * 10^4 and 4 * 10^4 meetings: half form one chain at time
1 listed in shuffled order, so passing the secret along by repeated sweeps of that time's meetings
(in either direction) takes ~10^4 sweeps, ~2 * 10^8 steps; the rest are at distinct times."""

SEEDS = 2
N = 4 * 10**4
M = 4 * 10**4


def generate(rng):
    first = rng.randrange(1, N)
    people = [p for p in range(N) if p not in (0, first)]
    rng.shuffle(people)
    chain = [rng.choice([0, first]), *people[: M // 2]]
    meetings = [[chain[i + 1], chain[i], 1] for i in range(M // 2)]
    rng.shuffle(meetings)
    for i in range(M - M // 2):
        x, y = rng.sample(range(N), 2)
        meetings.append([x, y, 2 + i])
    for m in meetings:
        if rng.random() < 0.5:
            m[0], m[1] = m[1], m[0]
    return {"n": N, "meetings": meetings, "firstPerson": first}
