"""Maximum Performance of a Team with 5 * 10^4 random engineers and k between n / 2 and 9n / 10, so
picking or summing the fastest k afresh for each minimum efficiency is quadratic."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    speed = [rng.randint(1, 10**5) for _ in range(N)]
    efficiency = [rng.randint(1, 10**8) for _ in range(N)]
    return {"n": N, "speed": speed, "efficiency": efficiency, "k": rng.randint(N // 2, 9 * N // 10)}
