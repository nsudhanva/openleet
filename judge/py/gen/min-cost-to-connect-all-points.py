"""Min Cost to Connect All Points with 1000 distinct points: spread over [-10^6, 10^6] or
packed into a small square so many edges tie."""

SEEDS = 3
N = 1000


def generate(rng):
    half = rng.choice((10**6, 40))
    cells = rng.sample(range((2 * half + 1) ** 2), N)
    side = 2 * half + 1
    return {"points": [[c // side - half, c % side - half] for c in cells]}
