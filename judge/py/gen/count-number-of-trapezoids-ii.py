"""Count Number of Trapezoids II at 500 points spread over 2-3 parallel lines in a random direction
(4-6 * 10^4 segments share one slope), so testing every set of four points costs ~2.6 * 10^9
checks."""

SEEDS = 2
N = 500
BOX = 1000
DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, 2), (2, -1)]


def generate(rng):
    dx, dy = rng.choice(DIRECTIONS)
    lines = rng.randint(2, 3)
    inside = lambda x, y: -BOX <= x <= BOX and -BOX <= y <= BOX  # noqa: E731
    keys, chosen = set(), set()
    while len(keys) < lines:
        ox, oy = rng.randint(-BOX // 2, BOX // 2), rng.randint(-BOX // 2, BOX // 2)
        if dy * ox - dx * oy in keys:
            continue
        keys.add(dy * ox - dx * oy)
        line = [(ox + t * dx, oy + t * dy) for t in range(-2 * BOX, 2 * BOX + 1)]
        line = [p for p in line if inside(*p)]
        chosen.update(rng.sample(line, min(len(line), N // lines)))
    while len(chosen) < N:
        chosen.add((rng.randint(-BOX, BOX), rng.randint(-BOX, BOX)))
    points = [list(p) for p in sorted(chosen)]
    rng.shuffle(points)
    return {"points": points}
