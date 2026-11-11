"""Walls and Gates on a 250 x 250 maze: one corridor two cells wide snaking down (left to right,
then back), with 1500 gates along one side of its left-to-right stretches, so each gate in
row-major order is nearer to everything after it and flooding from one gate after another is
~3 * 10^7 cell updates."""

SEEDS = 2
M = N = 250
GATES = 1500
INF = 2**31 - 1


def generate(rng):
    rooms = []
    for r in range(M):
        if r % 6 in (2, 5):
            row = [-1] * N
            row[N - 1 if r % 6 == 2 else 0] = INF  # the turn at the corridor's end
            rooms.append(row)
        else:
            rooms.append([INF] * N)  # rows 0, 1 mod 6 run right, rows 3, 4 mod 6 back
    # Gates on the first row of each rightward stretch, leaving the second row to pass them.
    forward = [(r, c) for r in range(0, M, 6) for c in range(N)]
    for r, c in rng.sample(forward, GATES):
        rooms[r][c] = 0
    return {"rooms": rooms}
