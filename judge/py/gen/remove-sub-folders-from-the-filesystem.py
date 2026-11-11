"""Remove Sub-Folders from the Filesystem at 10^4 folders in a random directory tree, so testing
every folder against every other as a parent costs ~10^8 prefix checks."""

SEEDS = 2
N = 10**4


def generate(rng):
    letters = rng.choice(("ab", "abcdefghijklmnopqrstuvwxyz"))
    paths, seen = [], set()
    while len(paths) < N:
        base = rng.choice(paths) if paths and rng.random() < 0.8 else ""
        name = "".join(rng.choice(letters) for _ in range(rng.randint(1, 4)))
        path = f"{base}/{name}"
        if len(path) <= 100 and path not in seen:
            seen.add(path)
            paths.append(path)
    rng.shuffle(paths)
    return {"folder": paths}
