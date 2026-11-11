"""Three runs of 15 to 20 '+' in at most 60 characters, a losing start (Grundy values xor to
0), so memoised backtracking over whole boards faces up to ~10^11 states."""

SEEDS = 2
N = 60
# Run lengths whose Grundy values xor to 0, so the first player loses and every reply is searched.
LOSING = ((15, 20, 20), (15, 19, 20), (15, 19, 19), (15, 18, 18), (15, 17, 18))


def generate(rng):
    runs = list(LOSING[rng.randrange(len(LOSING))])
    rng.shuffle(runs)
    # One '-' between runs, plus spare ones before, between or after them.
    pad = [0, 1, 1, 0]
    for _ in range(rng.randint(0, N - sum(runs) - 2)):
        pad[rng.randrange(4)] += 1
    parts = ["-" * pad[0]]
    for r, gap in zip(runs, pad[1:], strict=True):
        parts += ["+" * r, "-" * gap]
    return {"currentState": "".join(parts)}
