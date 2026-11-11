"""Escape a Large Maze with <= 200 blocked squares forming a corner wall x + y = 199 around one end:
seed 0 has one gap (both ends free, far apart), seeds 1 and 2 seal the target or the source, so a
search that is not cut off after ~2 * 10^4 squares wanders the 10^12-square grid."""

SEEDS = 3
B = 200
SIZE = 10**6


def generate(rng):
    r = rng.random()
    # The wall x + y = B - 1 seals every square with x + y < B - 1 into the corner.
    blocked = [[i, B - 1 - i] for i in range(B)]
    if r >= 0.5 and r < 0.9:
        blocked.pop(rng.randrange(1, B - 1))
    ix = rng.randrange(B - 1)
    inside = [ix, rng.randrange(B - 1 - ix)]
    outside = [rng.randrange(SIZE // 2, SIZE), rng.randrange(SIZE // 2, SIZE)]
    source, target = (inside, outside) if r >= 0.9 else (outside, inside)
    # Mirror the picture into a random corner.
    fx, fy = rng.random() < 0.5, rng.random() < 0.5

    def flip(p):
        return [SIZE - 1 - p[0] if fx else p[0], SIZE - 1 - p[1] if fy else p[1]]

    blocked = [flip(p) for p in blocked]
    rng.shuffle(blocked)
    return {"blocked": blocked, "source": flip(source), "target": flip(target)}
