"""Number of Paths with Max Score on a 100 x 100 board: one with scattered obstacles, one of
all digits so the path counts grow huge and must be taken modulo 10^9 + 7."""

SEEDS = 2
N = 100


def generate(rng):
    blocked = rng.choice([0.0, 0.15])
    rows = []
    for r in range(N):
        row = []
        for c in range(N):
            if r == 0 and c == 0:
                row.append("E")
            elif r == N - 1 and c == N - 1:
                row.append("S")
            elif rng.random() < blocked:
                row.append("X")
            else:
                row.append(str(rng.randint(1, 9)))
        rows.append("".join(row))
    return {"board": rows}
