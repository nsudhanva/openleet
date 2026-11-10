"""Asteroid Collision at n = 10^4: a run of right-movers then left-movers that destroy them one
by one (stack fully unwinds), or random sizes and directions."""

SEEDS = 3
N = 10**4


def generate(rng):
    shape = rng.choice(["unwind", "random", "equal"])
    if shape == "unwind":
        half = N // 2
        right = [rng.randint(1, 999) for _ in range(half)]
        left = [-rng.randint(1, 1000) for _ in range(N - half - 1)] + [-1000]
        asteroids = right + left
    elif shape == "equal":
        size = rng.randint(1, 1000)
        asteroids = [size] * (N // 2) + [-size] * (N // 2)
    else:
        asteroids = [rng.choice([1, -1]) * rng.randint(1, 1000) for _ in range(N)]
    return {"asteroids": asteroids}
