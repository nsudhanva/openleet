"""Count Number of Trapezoids I at 3 * 10^4 points on ~1.4 * 10^4 horizontal lines (two or three
each), so pairing every two lines costs ~10^8 steps."""

SEEDS = 2
N = 3 * 10**4
LIMIT = 10**8


def generate(rng):
    points, used = [], set()
    while len(points) < N:
        y = rng.randint(-LIMIT, LIMIT)
        if y in used:
            continue
        used.add(y)
        size = min(N - len(points), rng.choice((2, 2, 2, 3)))
        points += [[x, y] for x in rng.sample(range(-LIMIT, LIMIT + 1), size)]
    rng.shuffle(points)
    return {"points": points}
