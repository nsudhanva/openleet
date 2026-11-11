"""Delete Duplicate Folders with 2 * 10^4 folders: top-level folders each holding the chain
a/a/.../<3-letter leaf>, alike down to the leaf and a tenth repeating an earlier one, so comparing
each folder with every distinct one seen so far costs ~10^8 comparisons."""

SEEDS = 2
FOLDERS = 2 * 10**4
DEPTH = 4  # folders per chain under each top-level folder


def generate(rng):
    letters = "abcdefghijklmnopqrstuvwxyz"
    roots, leaves, paths = set(), [], []
    while len(paths) + DEPTH + 1 <= FOLDERS:
        root = "".join(rng.choices(letters, k=4))
        if root in roots:
            continue
        roots.add(root)
        if leaves and rng.random() < 0.1:
            leaf = rng.choice(leaves)
        else:
            leaf = "".join(rng.choices(letters, k=3))
        leaves.append(leaf)
        chain = [root] + ["a"] * (DEPTH - 1) + [leaf]
        paths += [chain[: i + 1] for i in range(DEPTH + 1)]
    rng.shuffle(paths)
    return {"paths": paths}
