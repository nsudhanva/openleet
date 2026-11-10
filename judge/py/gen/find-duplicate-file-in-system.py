"""Find Duplicate File in System near the 5 * 10^5 total-length cap: either 10^4+ small
directories or a few hundred directories packed with files, contents drawn from a small pool
so duplicate groups are large."""

from _shapes import random_string

SEEDS = 2
BUDGET = 490_000
ALPHA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def generate(rng):
    many_dirs = rng.random() < 0.5
    pool = [random_string(rng, ALPHA, rng.randint(1, 30)) for _ in range(200)]
    paths, total, d = [], 0, 0
    while len(paths) < 2 * 10**4:
        depth = rng.randint(0, 3)
        directory = "root" + "".join(f"/d{d}x{i}" for i in range(depth)) if depth else "root"
        if depth == 0 and d > 0:
            directory = f"root/top{d}"
        d += 1
        parts = [directory]
        length = len(directory)
        files = rng.randint(1, 5) if many_dirs else rng.randint(50, 120)
        for f in range(files):
            piece = f" f{f}.txt({rng.choice(pool)})"
            if length + len(piece) > 3000:
                break
            parts.append(piece)
            length += len(piece)
        if total + length > BUDGET:
            break
        paths.append("".join(parts))
        total += length
    return {"paths": paths}
