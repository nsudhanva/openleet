"""Grid Teleportation Traversal on a 200 x 200 grid: the top half holds ~10^4 portals of one to
three letters, the bottom half a walled snake to the target, so every portal is reached before
the target and re-scanning a letter's portals on each visit costs ~10^7 or more steps."""

from string import ascii_uppercase

SEEDS = 2
M = 200
N = 200


def generate(rng):
    letters = ascii_uppercase[: rng.randint(1, 3)]
    top = M // 2
    if (M - 1 - top) % 2 == 0:
        top += 1
    rows = []
    for _ in range(top):
        row = []
        for _ in range(N):
            r = rng.random()
            row.append(rng.choice(letters) if r < 0.5 else "#" if r < 0.55 else ".")
        rows.append(row)
    rows[0][0] = "."
    for r in range(top, M):
        if (r - top) % 2 == 0:
            row = ["#"] * N
            row[0 if (r - top) // 2 % 2 == 0 else N - 1] = "."
        else:
            row = ["."] * N
        rows.append(row)
    return {"matrix": ["".join(row) for row in rows]}
