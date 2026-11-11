"""Meeting Rooms II at the maximum 10^4 meetings that all span the midpoint, so 10^4 rooms are
needed and scanning the open rooms for each meeting costs ~5 * 10^7 checks."""

SEEDS = 2
N = 10**4
LIMIT = 10**6


def generate(rng):
    intervals = []
    for _ in range(N):
        a = rng.randrange(LIMIT // 2)
        intervals.append([a, rng.randint(LIMIT // 2 + 1, LIMIT)])
    return {"intervals": intervals}
