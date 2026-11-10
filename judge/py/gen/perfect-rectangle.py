"""Perfect Rectangle with 2 * 10^4 rectangles from random guillotine cuts of one big rectangle:
an exact cover, or the same cover with one piece shrunk (a gap) or duplicated (an overlap)."""

SEEDS = 3
N = 2 * 10**4


def generate(rng):
    x0, y0 = rng.randint(-(10**5), -(5 * 10**4)), rng.randint(-(10**5), -(5 * 10**4))
    x1, y1 = rng.randint(5 * 10**4, 10**5), rng.randint(5 * 10**4, 10**5)
    rects = [[x0, y0, x1, y1]]
    while len(rects) < N:
        i = rng.randrange(len(rects))
        a, b, c, d = rects[i]
        if c - a < 2 and d - b < 2:
            continue
        if c - a >= 2 and (d - b < 2 or rng.random() < 0.5):
            m = rng.randint(a + 1, c - 1)
            rects[i] = [a, b, m, d]
            rects.append([m, b, c, d])
        else:
            m = rng.randint(b + 1, d - 1)
            rects[i] = [a, b, c, m]
            rects.append([a, m, c, d])
    roll = rng.random()
    if roll < 0.35:
        for r in rects:
            if r[2] - r[0] >= 2:
                r[2] -= 1
                break
    elif roll < 0.7:
        rects[rng.randrange(N)] = list(rects[rng.randrange(N)])
    rng.shuffle(rects)
    return {"rectangles": rects}
