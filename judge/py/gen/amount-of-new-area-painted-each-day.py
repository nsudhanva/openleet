"""Amount of New Area Painted on [0, 5 * 10^4]: 2 * 10^4 strokes over 80% of the line (walking
every unit is ~9 * 10^8 steps), or 2.5 * 10^4 separate unit pieces then 3.5 * 10^4 repaints and
gap fills that keep ~2 * 10^4 pieces apart (scanning a list of painted pieces is ~7 * 10^8)."""

SEEDS = 2
WIDE = 2 * 10**4
REPAINTS = 35 * 10**3
END = 5 * 10**4


def generate(rng):
    paint = []
    if rng.random() > 0.5:  # seed 0
        for _ in range(WIDE):
            width = rng.randint(END * 4 // 5, END)
            start = rng.randint(0, END - width)
            paint.append([start, start + width])
        return {"paint": paint}
    pieces = END // 2
    order = list(range(pieces))
    rng.shuffle(order)
    paint = [[2 * i, 2 * i + 1] for i in order]
    for _ in range(REPAINTS):
        i = rng.randrange(pieces - 1)
        paint.append([2 * i, 2 * i + 1] if rng.random() < 0.75 else [2 * i + 1, 2 * i + 2])
    return {"paint": paint}
