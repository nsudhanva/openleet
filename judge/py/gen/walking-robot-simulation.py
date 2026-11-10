"""Walking Robot Simulation with 10^4 commands and 10^4 obstacles, many of them on the robot's
own path so it keeps bumping; total travel capped so the answer stays below 2^31."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4
TRAVEL = 46000  # 46000^2 < 2^31
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def generate(rng):
    shape = pick_shape(rng)
    commands, travel = [], 0
    for _ in range(N):
        if rng.random() < (0.2 if shape == 0 else 0.4):
            commands.append(rng.choice([-1, -2]))
        else:
            k = rng.randint(1, 9)
            if travel + k > TRAVEL:
                commands.append(-1)
            else:
                commands.append(k)
                travel += k
    # Walk without obstacles and drop obstacles on some of the visited cells.
    x = y = d = 0
    visited = []
    for c in commands:
        if c == -1:
            d = (d + 1) % 4
        elif c == -2:
            d = (d + 3) % 4
        else:
            for _ in range(c):
                x, y = x + DIRS[d][0], y + DIRS[d][1]
                if abs(x) <= 3 * 10**4 and abs(y) <= 3 * 10**4:
                    visited.append((x, y))
    on_path = set(rng.sample(visited, min(len(visited) // 4, N // 2)))
    on_path.discard((0, 0))
    obstacles = set(on_path)
    while len(obstacles) < N:
        obstacles.add((rng.randint(-(3 * 10**4), 3 * 10**4), rng.randint(-(3 * 10**4), 3 * 10**4)))
    if shape == 2:
        obstacles.discard(next(iter(sorted(obstacles))))
        obstacles.add((0, 0))  # allowed: ignored until the robot leaves the origin
    else:
        obstacles.discard((0, 0))
    obstacles = [list(p) for p in sorted(obstacles)]
    rng.shuffle(obstacles)
    return {"commands": commands, "obstacles": obstacles}
