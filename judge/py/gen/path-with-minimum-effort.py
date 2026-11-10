"""Path With Minimum Effort on a 100 x 100 grid: random heights, or a winding low-effort
corridor through high walls so the best path is long."""

SEEDS = 2
SIZE = 100


def generate(rng):
    if rng.random() < 0.5:
        heights = [[rng.randint(1, 10**6) for _ in range(SIZE)] for _ in range(SIZE)]
    else:
        heights = [[rng.randint(5 * 10**5, 10**6) for _ in range(SIZE)] for _ in range(SIZE)]
        # Serpentine corridor: even rows fully open, odd rows open at alternating ends.
        for r in range(SIZE):
            for c in range(SIZE):
                gap = SIZE - 1 if (r // 2) % 2 == 0 else 0
                if r % 2 == 0 or c == gap:
                    heights[r][c] = rng.randint(1, 50)
    return {"heights": heights}
