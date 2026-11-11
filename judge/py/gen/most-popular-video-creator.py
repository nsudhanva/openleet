"""Most Popular Video Creator at n = 2 * 10^4 videos by ~10^4 distinct creators, two of them tied
on top with equal-view videos, so summing each creator's views by a full scan is ~2 * 10^8
steps."""

SEEDS = 2
N = 2 * 10**4
STAR = 20
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def name(rng):
    return "".join(rng.choice(LETTERS) for _ in range(rng.randint(1, 5)))


def generate(rng):
    stars = [name(rng) for _ in range(2)]
    while stars[0] == stars[1]:
        stars[1] = name(rng)
    pool = [name(rng) for _ in range(N // 2)]
    pool = [c for c in pool if c not in stars]
    rows = [(rng.choice(pool), name(rng), rng.randint(0, 10**5)) for _ in range(N - 2 * STAR)]
    views = [rng.choice((10**5, 10**5 - 1)) for _ in range(STAR)]
    for star in stars:
        rows += [(star, name(rng), v) for v in views]
    rng.shuffle(rows)
    return {
        "creators": [r[0] for r in rows],
        "ids": [r[1] for r in rows],
        "views": [r[2] for r in rows],
    }
