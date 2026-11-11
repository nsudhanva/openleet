"""Four or five runs of 5 to 20 '+' filling nearly all of the 60 characters, a losing start
(Grundy values xor to 0): memoised backtracking, even keyed by the sorted run lengths, visits
~6 * 10^4 states per seed, and 6 seeds put it past the time limit."""

SEEDS = 6
N = 60
# Run lengths whose Grundy values xor to 0, so the first player loses and every reply is searched.
LOSING = (
    (10, 14, 16, 17),
    (6, 16, 16, 19),
    (6, 13, 18, 20),
    (10, 14, 14, 19),
    (12, 13, 16, 16),
    (5, 6, 12, 13, 20),
    (11, 12, 13, 20),
    (6, 12, 18, 20),
    (6, 7, 10, 13, 20),
    (9, 15, 16, 16),
)


def generate(rng):
    runs = list(LOSING[rng.randrange(len(LOSING))])
    rng.shuffle(runs)
    # One '-' between runs, plus spare ones before, between or after them.
    pad = [0] + [1] * (len(runs) - 1) + [0]
    for _ in range(rng.randint(0, N - sum(runs) - len(runs) + 1)):
        pad[rng.randrange(len(pad))] += 1
    parts = ["-" * pad[0]]
    for r, gap in zip(runs, pad[1:], strict=True):
        parts += ["+" * r, "-" * gap]
    return {"currentState": "".join(parts)}
