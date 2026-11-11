"""Remove Sub-Folders from the Filesystem at 4 * 10^4 folders: a random directory tree where 80 %
of folders sit inside an earlier one, or mostly separate top-level folders (10 % nested). Testing
every folder against every other as a parent costs ~10^9 prefix checks, and testing each against
every kept root costs ~7 * 10^8 on the second shape, where ~3.6 * 10^4 roots stay."""

from _shapes import pick_shape

SEEDS = 2
N = 4 * 10**4


def generate(rng):
    letters = rng.choice(("ab", "abcdefghijklmnopqrstuvwxyz"))
    nest = 0.8 if pick_shape(rng) == 0 else 0.1
    paths, seen = [], set()
    while len(paths) < N:
        inside = bool(paths) and rng.random() < nest
        base = rng.choice(paths) if inside else ""
        size = rng.randint(1, 4) if inside or nest > 0.5 else rng.randint(5, 12)
        name = "".join(rng.choice(letters) for _ in range(size))
        path = f"{base}/{name}"
        if len(path) <= 100 and path not in seen:
            seen.add(path)
            paths.append(path)
    rng.shuffle(paths)
    return {"folder": paths}
