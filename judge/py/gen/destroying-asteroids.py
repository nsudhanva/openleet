"""Destroying Asteroids with 10^5 asteroids: a set the planet can just barely absorb in sorted
order (answer true after a full pass), or random masses with one giant asteroid."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        mass = rng.randint(1, 10)
        cur, asteroids = mass, []
        for _ in range(N):
            a = rng.randint(1, min(10**5, cur))
            asteroids.append(a)
            cur += a
        rng.shuffle(asteroids)
    else:
        mass = rng.randint(1, 10**5)
        asteroids = [rng.randint(1, 10**5) for _ in range(N)]
    return {"mass": mass, "asteroids": asteroids}
