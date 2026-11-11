"""Count Positions on Street With Required Brightness at n = 2 * 10^4 positions and 2 * 10^4
lights whose ranges mostly span the street, so lighting each covered position one by one costs
~4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
RANGE = 10**5


def generate(rng):
    lights = [[rng.randrange(N), rng.randint(N // 4, RANGE)] for _ in range(N)]
    requirement = [rng.randint(N // 2, N) for _ in range(N)]
    return {"n": N, "lights": lights, "requirement": requirement}
