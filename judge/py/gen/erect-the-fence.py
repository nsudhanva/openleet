"""Erect the Fence with 3000 unique points in the 101 x 101 grid: random points, or many
points on the border of a rectangle so collinear hull points must all be kept."""

SEEDS = 2
N = 3000


def generate(rng):
    cells = rng.sample(range(101 * 101), N)
    trees = [[c // 101, c % 101] for c in cells]
    if rng.random() < 0.5:
        border = [[x, 0] for x in range(101)] + [[x, 100] for x in range(101)]
        border += [[0, y] for y in range(1, 100)] + [[100, y] for y in range(1, 100)]
        seen = {(x, y) for x, y in border}
        inner = [p for p in trees if (p[0], p[1]) not in seen][: N - len(border)]
        trees = border + inner
        rng.shuffle(trees)
    return {"trees": trees}
