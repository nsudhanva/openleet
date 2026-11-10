"""Rectangle Area II with 200 heavily overlapping rectangles at coordinates up to 10^9, so the
area overflows 32 bits and grid-cell counting is hopeless."""

SEEDS = 2


def generate(rng):
    rects = []
    spread = rng.choice([10**9, 10**6])
    for _ in range(200):
        x1, x2 = sorted(rng.sample(range(0, spread + 1), 2))
        y1, y2 = sorted(rng.sample(range(0, spread + 1), 2))
        rects.append([x1, y1, x2, y2])
    return {"rectangles": rects}
