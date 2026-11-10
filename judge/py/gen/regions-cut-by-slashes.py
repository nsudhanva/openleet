"""Regions Cut By Slashes on the maximum 30 x 30 grid: random slashes, or a dense diamond
lattice with hundreds of tiny regions."""

SEEDS = 2
N = 30


def generate(rng):
    if rng.random() < 0.5:
        grid = ["".join(rng.choice("/\\ ") for _ in range(N)) for _ in range(N)]
    else:
        grid = [
            "".join(
                ("/" if (r + c) % 2 == 0 else "\\")
                if r % 2 == 0
                else ("\\" if (r + c) % 2 == 0 else "/")
                for c in range(N)
            )
            for r in range(N)
        ]
    return {"grid": grid}
