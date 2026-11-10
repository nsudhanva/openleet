"""Flood Fill on a 50 x 50 image with a winding single-color region from the start cell, colors
below 2^16, and sometimes a new color equal to the old one."""

SEEDS = 3
N = 50


def generate(rng):
    old = rng.randrange(2**16)
    other = (old + 1) % 2**16
    shape = rng.randrange(2)
    if shape == 0:
        # A serpentine corridor: the region is one long path through the grid.
        image = [[other] * N for _ in range(N)]
        for r in range(0, N, 2):
            for c in range(N):
                image[r][c] = old
            if r + 1 < N:
                image[r + 1][N - 1 if (r // 2) % 2 == 0 else 0] = old
    else:
        image = [[old if rng.random() < 0.7 else other for _ in range(N)] for _ in range(N)]
    sr, sc = 0, 0
    image[sr][sc] = old
    color = old if rng.random() < 0.3 else rng.randrange(2**16)
    return {"image": image, "sr": sr, "sc": sc, "color": color}
