"""Image Overlap at the maximum 30 x 30, random or one image a shifted copy of the other."""

SEEDS = 3
N = 30


def generate(rng):
    p = rng.choice([0.2, 0.5, 0.9])
    img1 = [[1 if rng.random() < p else 0 for _ in range(N)] for _ in range(N)]
    if rng.random() < 0.5:
        dr, dc = rng.randint(-N + 1, N - 1), rng.randint(-N + 1, N - 1)
        img2 = [
            [img1[r - dr][c - dc] if 0 <= r - dr < N and 0 <= c - dc < N else 0 for c in range(N)]
            for r in range(N)
        ]
    else:
        img2 = [[1 if rng.random() < p else 0 for _ in range(N)] for _ in range(N)]
    return {"img1": img1, "img2": img2}
